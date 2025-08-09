from fastapi import FastAPI
from gallery_recommender.infrastructure.inference_pipeline_api import app, recommend_router, exhibition_reports_router  # noqa
from gallery_recommender.infrastructure.data_service_api import data_router
from gallery_recommender.infrastructure.inference_pipeline_api import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(recommend_router)
app.include_router(exhibition_reports_router)
app.include_router(data_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("tools.ml_service:app", host="0.0.0.0", port=8080, reload=True)