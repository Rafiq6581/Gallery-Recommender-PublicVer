from gallery_recommender.infrastructure.inference_pipeline_api import app  # noqa

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("tools.exhibition_reports_service:app", host="0.0.0.0", port=8080, reload=True)