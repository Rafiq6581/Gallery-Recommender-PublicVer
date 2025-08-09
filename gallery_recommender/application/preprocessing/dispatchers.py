from loguru import logger 

from gallery_recommender.domain.base import NoSQLBaseData, VectorBaseData
from gallery_recommender.domain.types import DataCategory


from .cleaning_data_handlers import (
    CleaningDataHandler,
    ExhibitionCleaningHandler,
    ReflectionCleaningHandler,
)

from .embedding_data_handlers import (
    EmbeddingDataHandler,
    ExhibitionEmbeddingHandler,
    ReflectionEmbeddingHandler,
    QueryEmbeddingHandler,
)


class CleaningHandlerFactory:
    @staticmethod
    def create_handler(data_category: DataCategory) -> CleaningDataHandler:
        if data_category == DataCategory.EXHIBITION:
            return ExhibitionCleaningHandler()
        elif data_category == DataCategory.REFLECTION:
            return ReflectionCleaningHandler()
        else:
            raise ValueError(f"No cleaning handler found for data category: {data_category}")
        

class CleaningDispatcher:
    cleaning_factory = CleaningHandlerFactory()

    @classmethod
    def dispatch(cls, data_model: NoSQLBaseData) -> VectorBaseData:
        data_category = DataCategory(data_model.get_collection_name())
        handler = cls.cleaning_factory.create_handler(data_category)
        clean_model = handler.clean(data_model)

        logger.info(
            "Document cleaned successfully",
            data_category=data_category,
            cleaned_content_len=len(clean_model.description),
        )

        return clean_model
    

class EmbeddingHandlerFactory:
    @staticmethod
    def create_handler(data_category: DataCategory) -> EmbeddingDataHandler:
        if data_category == DataCategory.QUERIES:
            return QueryEmbeddingHandler()
        elif data_category == DataCategory.EXHIBITION:
            return ExhibitionEmbeddingHandler()
        elif data_category == DataCategory.REFLECTION:
            return ReflectionEmbeddingHandler()
        else:
            raise ValueError(f"No embedding handler found for data category: {data_category}")
        

class EmbeddingDispatcher:
    embedding_factory = EmbeddingHandlerFactory()

    @classmethod
    def dispatch(
        cls, data_model: VectorBaseData | list[VectorBaseData]
    ) -> VectorBaseData | list[VectorBaseData]:
        is_list = isinstance(data_model, list)
        if not is_list:
            data_model = [data_model]

        if len(data_model) == 0:
            return []
        
        data_category = data_model[0].get_category()
        assert all(
            data_model.get_category() == data_category for data_model in data_model
        ), "All data models must be of the same category"

        handler = cls.embedding_factory.create_handler(data_category)
        embedding_model = handler.embed_batch(data_model)

        if not is_list:
            embedding_model = embedding_model[0]

        logger.info(
            "Document embedded successfully",
            data_category=data_category,
        )

        return embedding_model