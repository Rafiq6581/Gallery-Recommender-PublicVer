from gallery_recommender.infrastructure.data_service_api import app  # noqa

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("tools.data_service:app", host="0.0.0.0", port=8081, reload=True)