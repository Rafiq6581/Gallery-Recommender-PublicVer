from loguru import logger
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from gallery_recommender.settings import settings

class MongoDatabaseConnector:
    _instance: MongoClient | None = None

    def __new__(cls, *args, **kwargs) -> MongoClient:
        if cls._instance is None:
            try:
                cls._instance = MongoClient(settings.DATABASE_HOST)
            except ConnectionFailure as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise

        logger.info(f"Connected to MongoDB: {settings.DATABASE_HOST}")

        return cls._instance
    
connection = MongoDatabaseConnector()