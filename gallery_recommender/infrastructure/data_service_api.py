from fastapi import FastAPI, APIRouter
from datetime import datetime
from fastapi.responses import JSONResponse
from bson.json_util import dumps
from collections import defaultdict

from gallery_recommender.domain import ExhibitionData

app = FastAPI()
data_router = APIRouter()
ExhibitionModel = ExhibitionData

@data_router.get("/exhibitions/active")
def get_active_exhibitions():
    now = datetime.now()
    active_cursor = ExhibitionModel.bulk_find({"exhibition_end_date": {"$gte": now}})

    grouped = defaultdict(list)

    for doc in active_cursor:
        area = getattr(doc, "area", "")
        grouped[area].append({
            "uid": str(getattr(doc, "id", "")),
            "name": getattr(doc, "name", "") if getattr(doc, "name", None) else "",
            "Latitude": getattr(doc, "latitude", ""),
            "Longitude": getattr(doc, "longitude", ""),
            "exhibition_start_date": getattr(doc, "exhibition_start_date", "").isoformat() if getattr(doc, "exhibition_start_date", None) else None,
            "exhibition_end_date": getattr(doc, "exhibition_end_date", "").isoformat() if getattr(doc, "exhibition_end_date", None) else None,
            "exhibition_image_url": getattr(doc, "exhibition_image_url", ""),
        })

    response = [
        {
            "area": area,
            "count": len(exhibitions),
            "data": exhibitions
        }
        for area, exhibitions in grouped.items()
    ]

    return JSONResponse(content=response)

@app.get("/exhibitions/all")
def get_all_exhibitions():
    return JSONResponse(content=dumps(ExhibitionModel.find()))

@app.get("/exhibitions/{exhibition_id}")
def get_exhibition(exhibition_id: str):
    return JSONResponse(content=dumps(ExhibitionModel.find_one({"_id": ObjectId(exhibition_id)})))