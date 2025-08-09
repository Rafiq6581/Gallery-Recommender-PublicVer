from loguru import logger
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import PayloadSchemaType



from gallery_recommender.settings import settings

class QdrantDatabaseConnector:
    _instance: QdrantClient | None = None
    _last_info = {}

    def __new__(cls, *args, **kwargs) -> QdrantClient:
        if cls._instance is None:
            try:
                if settings.USE_QDRANT_CLOUD:
                    api_key = settings.QDRANT_APIKEY
                    # Mask the API key except last 4 chars
                    api_key_masked = f"{api_key[:4]}...{api_key[-4:]}" if api_key else None
                    cls._last_info = {
                    "mode": "cloud",
                    "uri": settings.QDRANT_CLOUD_URL,
                    "api_key": api_key_masked,
                    }
                    cls._instance = QdrantClient(
                        url=settings.QDRANT_CLOUD_URL,
                        api_key=api_key,
                    )
                    uri = settings.QDRANT_CLOUD_URL

                    logger.info(
                        f"Connection to Qdrant CLOUD: {uri} | API key: {api_key_masked}"
                    )
                else:
                    cls._last_info = {
                    "mode": "local",
                    "uri": f"{settings.QDRANT_DATABASE_HOST}:{settings.QDRANT_DATABASE_PORT}",
                    "api_key": None,
                    }
                    cls._instance = QdrantClient(
                        host=settings.QDRANT_DATABASE_HOST,
                        port=settings.QDRANT_DATABASE_PORT,
                    )
                    uri = f"{settings.QDRANT_DATABASE_HOST}:{settings.QDRANT_DATABASE_PORT}"

                    logger.info(
                        f"Connection to Qdrant LOCAL: {uri} | No API key required."
                    )
            except UnexpectedResponse:
                logger.exception(
                    "Couldn't connect to Qdrant.",
                    host=settings.QDRANT_DATABASE_HOST,
                    port=settings.QDRANT_DATABASE_PORT,
                    url=settings.QDRANT_CLOUD_URL,
                )
                raise

        return cls._instance
    
    @classmethod
    def get_connection_info(cls):
        return cls._last_info
    

    
connection = QdrantDatabaseConnector()