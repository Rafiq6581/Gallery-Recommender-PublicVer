import re 
from typing import List, Type

from loguru import logger

from gallery_recommender.domain.types import DataCategory

from .retriever_data_handlers import (
    RetrieverDataHandler,
    ExhibitionRetrieverDataHandler,
    ReflectionRetrieverDataHandler,
)

class RetrieverDataHandlerFactory:
    @staticmethod
    def create_handler(data_category: DataCategory) -> RetrieverDataHandler:
        if data_category == DataCategory.EXHIBITION:
            return ExhibitionRetrieverDataHandler()
        elif data_category == DataCategory.REFLECTION:
            return ReflectionRetrieverDataHandler()
        else:
            raise ValueError(f"No retriever data handler found for data category: {data_category}")
        

class RetrieverDispatcher:
    retriever_factory = RetrieverDataHandlerFactory()