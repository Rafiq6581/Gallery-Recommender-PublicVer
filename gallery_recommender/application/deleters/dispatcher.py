from loguru import logger
from .base import BaseDeleter

from .MongodbDeleter import MongodbDeleter
from .QdrantDeleter import QdrantDeleter

class DeleterDispatcher:
    def __init__(self) -> None:
        self._deleters = {}

    @classmethod
    def build(cls) -> "DeleterDispatcher":
        dispatcher = cls()

        return dispatcher
    
    def register_mongodb(self) -> "DeleterDispatcher":
        self.register("mongodb", MongodbDeleter)

        return self
    
    def register_qdrant(self) -> "DeleterDispatcher":
        self.register("qdrant", QdrantDeleter)

        return self
    
    def register(self, key: str, deleter: BaseDeleter) -> None:
        self._deleters[key] = deleter

    def get_deleter(self, collection_name: str) -> BaseDeleter:
        # Dispatch QdrantDeleter if keywords found
        keywords = ["cleaned", "embedded"]
        if any(word in collection_name for word in keywords):
            return QdrantDeleter()
        else:
            return MongodbDeleter()

