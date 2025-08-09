import uuid
from abc import ABC
from typing import Generic, Type, TypeVar
from loguru import logger
from pydantic import BaseModel, Field
from pymongo import errors

from gallery_recommender.domain.exceptions import ImproperlyConfigured
from gallery_recommender.infrastructure.db.mongo import connection
from gallery_recommender.settings import settings

T = TypeVar("T", bound="NoSQLBaseData")

# establishing a connection to the database
_database = connection.get_database(settings.DATABASE_NAME)

# all the other data classes will inherit from this class to interact with the NoSQL database
class NoSQLBaseData(BaseModel, Generic[T], ABC):
    # ensuring that every instance of a document has a unique ID
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    # ensuring that two documents are equal if they have the same ID
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id
    
    # ensuring that a document is hashable for the purpose of being used as a key in a dictionary
    def __hash__(self) -> int:
        return hash(self.id)
    

    @classmethod
    def from_mongo(cls: Type[T], data: dict) -> T:
        if not data:
            raise ValueError("Data is Empty")
        _id = data.pop("_id")
        return cls(**dict(data, id=uuid.UUID(str(_id))))
    
    def to_mongo(self: T, **kwargs) -> dict:
        # Use model_dump to convert the model to a dict.
        exclude_unset = kwargs.pop("exclude_unset", False)
        by_alias = kwargs.pop("by_alias", True)
        parsed = self.model_dump(exclude_unset=exclude_unset, by_alias=by_alias, **kwargs)
        
        # If there's an "id" key, remove it and set "_id" instead.
        if "_id" not in parsed and "id" in parsed:
            parsed["_id"] = str(parsed.pop("id"))
        
        # Ensure any UUIDs are converted to strings.
        for key, value in parsed.items():
            if isinstance(value, uuid.UUID):
                parsed[key] = str(value)
        
        return parsed
    
    # a method to dump the document to a dictionary
    def model_dump(self: T, **kwargs) -> dict:
        # modify the pydantic model dump method to convert UUID4 to string
        dict_ = super().model_dump(**kwargs)

        for key, value in dict_.items():
            if isinstance(value, uuid.UUID):
                dict_[key] = str(value)

        return dict_
    

    # a method to save the data to the database
    def save(self: T, **kwargs) -> T | None:
        # save the data to the database
        collection = _database.get_collection(self.get_collection_name())
        try:
            collection.insert_one(self.to_mongo(**kwargs))

            return self
        except errors.WriteError:
            logger.exception("Failed to insert data to the database")

            return None


    # a method to delete many documents from the database
    @classmethod
    def delete_mongodb(cls: Type[T], **kwargs) -> T | None:
        collection = _database.get_collection(cls.get_collection_name())
        try:
            collection.delete_many(kwargs)
            return cls
        except errors.OperationFailure:
            logger.exception("Failed to delete data from the database")

            return None
        
        
    # a method to delete a single document from the database
    def delete_one(self: T, **kwargs) -> bool:
        collection = _database.get_collection(self.get_collection_name())
        try:
            collection.delete_one(kwargs)
            return True
        except errors.OperationFailure:
            logger.exception("Failed to delete data from the database")

            return False
        
    @classmethod
    def get_or_create(cls: Type[T], **filter_options) -> T:
        collection = _database.get_collection(cls.get_collection_name())
        try:
            instance = collection.find_one(filter_options)
            if instance:
                return cls.from_mongo(instance)
        
            new_instance = cls(**filter_options)
            new_instance.save()

            return new_instance
        
        except errors.OperationFailure:
            logger.error(f"Failed to retrieve data with filtered options: {filter_options}")

            raise 


    # a method to bulk insert data to the database
    @classmethod 
    def bulk_insert(cls: Type[T], data: list[T], **kwargs) -> bool:
        collection = _database[cls.get_collection_name()]
        try:
            collection.insert_many(data.to_mongo(**kwargs) for data in data)

            return True
        except (errors.BulkWriteError, errors.WriteError):
            logger.exception(f"Failed to insert data of type: {cls.__name__}")

            return False
        

    # a method to find data in the database
    @classmethod
    def find(cls: Type[T], filter_dict: dict = None, **filter_options) -> T | None:
        collection = _database[cls.get_collection_name()]
        try:
            query = filter_dict or filter_options
            instance = collection.find_one(query)

            if instance:
                return cls.from_mongo(instance)
            
            return None
        
        except errors.OperationFailure:
            logger.error("Failed to retrieve data")

            return None
        

    # a method to bulk find data in the database
    @classmethod
    def bulk_find(cls: Type[T], filter_dict: dict = None, **filter_options) -> list[T]:
        try: 
            collection = _database[cls.get_collection_name()]
            query = filter_dict or filter_options
            instances = collection.find(query)
            return [data for instance in instances if (data := cls.from_mongo(instance)) is not None]
        
        except errors.OperationFailure:
            logger.error("Failed to retrieve data")

            return []
        

    @classmethod
    def get_collection_name(cls: Type[T]) -> str:
        # get the collection name from the class name
        if not hasattr(cls, "Settings") or not hasattr(cls.Settings, "name"):
            raise ImproperlyConfigured(
                f"Collection name not found in {cls.__name__}.Settings")
        
        return cls.Settings.name
