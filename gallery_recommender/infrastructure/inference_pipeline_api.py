from loguru import logger
import os
import datetime
from openai import OpenAI, AsyncOpenAI
from comet_ml import Experiment
from opik.integrations.openai import track_openai
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel
import opik
from typing import Optional, Dict, List, Union
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from gallery_recommender.infrastructure.gcp.deploy.cloud_tasks import create_task
from gallery_recommender.infrastructure.gcp.deploy.storage import save_report, fetch_report, delete_report   
import json

from gallery_recommender import settings
from gallery_recommender.application.rag import ContextRetriever
from gallery_recommender.infrastructure.db.qdrant import QdrantDatabaseConnector
from gallery_recommender.model.inference import InferenceExecutor, ChatGPTInference
from gallery_recommender.application.utils import misc
from gallery_recommender.infrastructure.opik_utils import configure_opik
from gallery_recommender.domain.data import GalleryData, ExhibitionData, ReflectionData
from gallery_recommender.domain.embedded_cleaned_data import EmbeddedExhibitionDocument
from gallery_recommender.application.rag.prompt_templates import ExhibitionReportTemplate, RecommendationTemplate, UnlistedExhibitionReportTemplate

os.environ["TOKENIZERS_PARALLELISM"] = "false"
GalleryModel = GalleryData
ExhibitionModel = ExhibitionData

# 1) configure Opik → Comet
configure_opik()  
# exp = Experiment(
#     api_key=os.environ["COMET_API_KEY"],
#     project_name="gallery-recommender",
#     workspace="rafiq6581",
#     auto_param_logging=False,
#     auto_metric_logging=False,
# )

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "index.html"), encoding="utf-8") as f:
    html = f.read()


openai = OpenAI(api_key=settings.OPENAI_API_KEY)
# async_openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

# 2) instrument calls
def _chat_completion(**payload):
    return openai.chat.completions.create(**payload)

class OpenAIInference(ChatGPTInference):
    def inference(self) -> list[dict]:
        # Make a single, non-streaming chat completion call
        response =  _chat_completion(
            model=self.model_id,
            messages=[{"role":"user","content": self.payload["messages"][0]["content"]}],
            temperature=self.payload["temperature"],
            max_tokens=self.payload["max_tokens"],
            top_p=self.payload["top_p"],
            stream=False,
        )

        # Return the completed text
        return [{"generated_text": response.choices[0].message.content}]




def initialize_indices():
    filterable_fields = list(EmbeddedExhibitionDocument.model_fields.keys())

    for field in filterable_fields:
        try:
            QdrantDatabaseConnector._instance.create_payload_index(
            collection_name=EmbeddedExhibitionDocument.Config.name,
            field_name=field,
            field_type="keyword" if field != "exhibition_start_date_ts" and field != "exhibition_end_date_ts" else "float",  # or "integer", "float" as needed
            )
            logger.info(f"Created index for field: {field}")
        except Exception as e:
            logger.warning(f"Index for {field} may already exist or failed to create: {e}")




# app = FastAPI()
@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_indices()
    yield

app = FastAPI(lifespan=lifespan)
recommend_router = APIRouter()
exhibition_reports_router = APIRouter()

class QueryRequest(BaseModel):
    query: dict
    filters: Optional[Dict[str, str]] = None
    uid: Optional[str] = None
    create_report: Optional[bool] = False

class QueryResponse(BaseModel):
    report: dict

class StreamRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, str]] = None

@opik.track
def call_llm_service(query: dict, context: str, prompt_template: str, filters: dict = None) -> dict:
    llm = OpenAIInference(query, settings.OPENAI_MODEL_ID, openai.api_key)
    return InferenceExecutor(llm, query, filters or {}, context, prompt_template).execute()

# @opik.track
# def call_llm_service_with_logging(query: dict, context: str):
#     import asyncio
#     async def get_full_response():
#         last_item = None
#         async for item in stream_llm_service(query, context):
#             last_item = item  # or collect all if needed
#         return last_item
    
    # # -- TIME TRACKING START --
    # start_time = time.time()
    # result = asyncio.run(get_full_response())
    # end_time = time.time()
    # elapsed = end_time - start_time
    # print(f"[Timing] call_llm_service_with_logging took {elapsed:.2f} seconds")
    # # Optionally, you can log this to comet_ml:
    # exp.log_metric("llm_response_time", elapsed)
    # # -- TIME TRACKING END --
    
    # return result

# @opik.track
# async def stream_llm_service(query: dict, context: str):
#     llm = OpenAIInference(query, settings.OPENAI_MODEL_ID, openai.api_key)
#     async for item in InferenceExecutor(llm, query, context).execute():
#         yield item

@opik.track
def rag(query: dict) -> str:
    retriever = ContextRetriever(mock=False)
    docs = retriever.search(query, k=3)
    context = " ".join([d.description for d in docs])
    report= call_llm_service(query, filters, context)
    return report

# @app.get("/")
# async def web_app() -> HTMLResponse:
#     """
#     Web App
#     """
#     return HTMLResponse(html)



@recommend_router.post("/recommend")
async def recommend_endpoint(req: QueryRequest):
    # session_id = str(uuid.uuid4())
    try:
        retriever = ContextRetriever(mock=False)
        docs = retriever.search(req.query, k=10, filters=req.filters)
        flat_cards = []
        for doc in docs:
            gallery = {}
            try:
                gallery_id = str(doc.gallery_id)
                logger.info(f"Gallery ID: {gallery_id}")
                gallery = GalleryModel.find(_id=str(gallery_id))
                logger.info(f"Gallery found: {gallery}")
            except Exception as e:
                logger.info(f"Gallery not found: {e}")
                gallery = {}

            card = {
                "UID": str(getattr(doc, "id", "")),
                "descriptions": getattr(doc, "description", "") if doc else "",
                "Gallery Name English": getattr(gallery, "name_english", "") if gallery else "",
                "Exhibition Name English": getattr(doc, "exhibition_name_english", ""),
                "Exhibition Image URL": getattr(doc, "exhibition_image_url", ""),
                "Latitude": getattr(gallery, "latitude", "") if gallery else "",
                "Longitude": getattr(gallery, "longitude", "") if gallery else "",
            }
            flat_cards.append(card)
        
        # ---- Cloud Task ----
        # this is for generating the individual reports for each exhibition in the background
        for card in flat_cards:
            uid = card["UID"]
            try:
                logger.info(f"Query type before task: {type(req.query)}")
                create_task(uid, {"query": req.query}, create_report=False)
                logger.info(f"Task created for {uid}")
            except Exception as e:
                logger.error(f"Error in creating task for {uid}: {e}")

        # ---- Content generation ----
        context = " ".join(
            f"{{Exhibition Name: {d.name}, Description: {d.description}}} \n" for d in docs
        )

        try:    
            result = call_llm_service(req.query, context, RecommendationTemplate().create_template(), filters=req.filters) # returns dict
            logger.info(f"Result: {result!r}")
            return JSONResponse(content={
            "recommended_exhibitions": flat_cards,
            "report": result["report"]
        })
        except Exception as e:
            raise
        

    except Exception as e:
        logger.error(f"Error in recommend endpoint: {e}")
        raise
    


@exhibition_reports_router.post("/exhibition_reports")
async def exhibition_reports_endpoint(req: QueryRequest):
    try:
        query = req.query
        if isinstance(query, str):
            try:
                logger.info(f"Query is a string: {query}")
                query = json.loads(query)
                logger.warning("Query was a string — parsed into dict.")
            except Exception as e:
                logger.error(f"Failed to parse query string into JSON: {e}")
                raise HTTPException(status_code=400, detail="Invalid query format. Must be JSON object.")

        # if the report is not requested, return the cached report
        if req.create_report == False:
            cached_report = fetch_report(req.uid)
            if cached_report:
                logger.info(f"Cached report found for {req.uid}")
                return JSONResponse(content={"report": cached_report})
            else:
                logger.info(f"No cached report found for {req.uid}, generating new report")
                doc = ExhibitionModel.find(_id=req.uid)
                if doc:
                    context = (
                        f"Exhibition Name: {getattr(doc, 'name', '')}, "
                        f"Description: {getattr(doc, 'description', '')}, "
                        f"Exhibition Start Date: {getattr(doc, 'exhibition_start_date', '')}, "
                        f"Exhibition End Date: {getattr(doc, 'exhibition_end_date', '')}, "
                        f"artist_name: {getattr(doc, 'artist', '')}"
                    )
                    report = call_llm_service(
                        query, context, prompt_template=UnlistedExhibitionReportTemplate().create_template()
                    )
                    save_report(req.uid, report["report"])
                    return JSONResponse(content={"report": report["report"]})
                else:
                    return JSONResponse(content={"report": "Exhibition not found"})
        else:
            logger.info(f"Regenerate report is requested for {req.uid}")
            doc = ExhibitionModel.find(_id=req.uid)
            if doc:
                context = (
                    f"Exhibition Name: {getattr(doc, 'name', '')}, "
                    f"Description: {getattr(doc, 'description', '')}, "
                    f"Exhibition Start Date: {getattr(doc, 'exhibition_start_date', '')}, "
                    f"Exhibition End Date: {getattr(doc, 'exhibition_end_date', '')}, "
                    f"artist_name: {getattr(doc, 'artist', '')}"
                )
                report = call_llm_service(
                    query, context, prompt_template=UnlistedExhibitionReportTemplate().create_template()
                )
                save_report(req.uid, report["report"])
                return JSONResponse(content={"report": report["report"]})
            else:
                return JSONResponse(content={"report": "Exhibition not found"})


    except Exception as e:
        logger.error(f"Error in exhibition_reports endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")







# @app.post("/exhibition_reports")
# async def exhibition_reports_endpoint(req: QueryRequest, session_id: str):
#     # Exhibition UID should be in the request query
#     exhibition_id = req.query.get("UID")
#     if not exhibition_id:
#         raise HTTPException(status_code=400, detail="Missing exhibition UID in query.")

#     # Compose a unique cache key (per session and exhibition)
#     cache_key = f"report:{session_id}:{exhibition_id}"
#     cached_report = redis_client.get(cache_key)
#     if cached_report:
#         logger.info(f"Returning cached report for session {session_id}, exhibition {exhibition_id}")
#         return JSONResponse(content={"report": cached_report})

#     # Get the session context as before
#     context = redis_client.get(f"rec:{session_id}")
#     if context is None:
#         raise HTTPException(status_code=404, detail="Session not found")

#     try:
#         result = call_llm_service(req.query, req.filters, context, ExhibitionReportTemplate().create_template())  # returns dict
#         report = result["report"]
#         # Cache for 24 hours (adjust as you need)
#         redis_client.setex(cache_key, 86400, report)
#         logger.info(f"Cached new report for session {session_id}, exhibition {exhibition_id}")
#         return JSONResponse(content={"report": report})
#     except Exception as e:
#         logger.error(f"Error generating report for exhibition {exhibition_id}: {e}")
#         raise


# @app.websocket("/ws/rag")
# async def rag_websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         data = await websocket.receive_json()
#         retriever = ContextRetriever(mock=False)
#         print(f"Data: {data}")
        
#         docs = retriever.search(data, k=10, filters=data.get("filters"))
#         flat_cards = []
#         for doc in docs:
#             gallery = {}
#             try:
#                 gallery_id = str(doc.gallery_id)
#                 logger.info(f"Gallery ID: {gallery_id}")
#                 gallery = GalleryModel.find(_id=str(gallery_id))
#                 logger.info(f"Gallery found: {gallery}")
#             except Exception as e:
#                 logger.info(f"Gallery not found: {e}")
#                 gallery = {}

#             card = {
#                     "UID": str(getattr(doc, "id", "")),
#                     "descriptions": getattr(doc, "description", "") if doc else "",
#                     "Gallery Name English": getattr(gallery, "name_english", "") if gallery else "",
#                     "Gallery Name Japanese": getattr(gallery, "name_japanese", "") if gallery else "",
#                     "Gallery Image URL": getattr(gallery, "gallery_image_url", "") if gallery else "",
#                     "Exhibition Name English": getattr(doc, "exhibition_name_english", ""),
#                     "Exhibition Name Japanese": getattr(doc, "exhibition_name_japanese", ""),
#                     "Exhibition Start Date": getattr(doc, "start_date", ""),
#                     "Exhibition End Date": getattr(doc, "end_date", ""),
#                     "Exhibition Image URL": getattr(doc, "exhibition_image_url", ""),
#                     "Area": getattr(gallery, "area", "") if gallery else "",
#                     "Address English": getattr(gallery, "address_english", "") if gallery else "",
#                     "Address Japanese": getattr(gallery, "address_japanese", "") if gallery else "",
#                     "Hours": getattr(gallery, "hours", "") if gallery else "",
#                     "Days Open": getattr(gallery, "days_open", "") if gallery else "",
#                     "Latitude": getattr(gallery, "latitude", "") if gallery else "",
#                     "Longitude": getattr(gallery, "longitude", "") if gallery else "",
#                     "Phone Number": getattr(gallery, "phone_number", "") if gallery else "",
#                     "Website": getattr(gallery, "website", "") if gallery else "",
#             }
#             flat_cards.append(card)

#         # send the flat_cards to the client
#         await websocket.send_json(flat_cards)
            
#         context = " ".join(f"{{Exhibition Name: {d.name}, Description: {d.description}}} \n" for d in docs)
#         print(context)
#         # Now stream each chunk as it's generated
#         async for item in stream_llm_service(data, context):
#             print("Streaming item:", item)  # See the keys in each item
#             if "partial" in item:
#             # await websocket.send_json(item)
#                 await websocket.send_text(item["partial"])
#             elif "report" in item:
#                 await websocket.send_text(item["report"])

        

#         await websocket.close()
#     except WebSocketDisconnect:
#         print("WebSocket disconnected")
#     except Exception as e:
#         await websocket.close()
#         raise