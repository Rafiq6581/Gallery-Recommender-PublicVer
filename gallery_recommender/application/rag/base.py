from abc import ABC, abstractmethod
from typing import Any

from langchain.prompts import PromptTemplate
from pydantic import BaseModel

from gallery_recommender.domain.queries import Query


class PromptTemplateFactory(ABC, BaseModel):
    @abstractmethod
    # the mock parameter is used to create a mock prompt template for testing purposes, i.e. the model is not used
    def create_template(self, mock: bool = False) -> PromptTemplate:
        pass


class RAGStep(ABC):
    def __init__(self, mock: bool = False) -> None:
        self._mock = mock

    @abstractmethod
    def generate(self, query: Query, *args, **kwargs) -> Any:
        pass
    