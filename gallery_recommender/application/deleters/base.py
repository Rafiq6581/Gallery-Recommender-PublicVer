from abc import ABC, abstractmethod

class BaseDeleter(ABC):

    @abstractmethod
    def delete_many(self, collection_name: str) -> None:
        pass