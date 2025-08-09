from loguru import logger

from .base import BaseDeleter
from gallery_recommender.domain.data import GalleryData, ExhibitionData


class MongodbDeleter(BaseDeleter):

    GalleryModel = GalleryData
    ExhibitionModel = ExhibitionData

    def delete_many(self, collection_name: str) -> None:
        logger.info(f"Deleting {collection_name} data")
        if collection_name == self.GalleryModel.get_collection_name():
            self.GalleryModel.delete_mongodb()
        elif collection_name == self.ExhibitionModel.get_collection_name():
            self.ExhibitionModel.delete_mongodb()
        else:
            logger.error(f"Collection name {collection_name} not found")


    def delete_one(self, collection_name: str, **kwargs) -> None:
        logger.info(f"Deleting {collection_name} data")
        if collection_name == self.GalleryModel.get_collection_name():
            self.GalleryModel.delete_one(**kwargs)
        elif collection_name == self.ExhibitionModel.get_collection_name():
            self.ExhibitionModel.delete_one(**kwargs)
        else:
            logger.error(f"Collection name {collection_name} not found")

    
