from loguru import logger


from .base import BaseDeleter
from gallery_recommender.domain.cleaned_data import CleanedExhibitionData
from gallery_recommender.domain.embedded_cleaned_data import EmbeddedExhibitionDocument

class QdrantDeleter(BaseDeleter):

    cleaned_exhibition_model = CleanedExhibitionData
    embedded_exhibition_model = EmbeddedExhibitionDocument


    def delete_many(self, collection_name: str) -> None:
        logger.info(f"Deleting {collection_name} data")
        if collection_name == self.cleaned_exhibition_model.get_collection_name():
            self.cleaned_exhibition_model.delete_qdrant(collection_name)
        elif collection_name == self.embedded_exhibition_model.get_collection_name():
            self.embedded_exhibition_model.delete_qdrant(collection_name)
        else:
            logger.error(f"Collection name {collection_name} not found")
            

