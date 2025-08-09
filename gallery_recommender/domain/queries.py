from pydantic import Field

from gallery_recommender.domain.data import DataCategory
from gallery_recommender.domain.base import VectorBaseData
from gallery_recommender.application.utils.misc import query_dict_to_str

class Query(VectorBaseData):
    content: dict | str
    metadata: dict = Field(default_factory=dict)

    class Config:
        category = DataCategory.QUERIES


    @classmethod
    def from_str(cls, query: str) -> "Query":
        return Query(content=query.strip("\n "))

    @classmethod
    def from_dict(cls, query: dict) -> "Query":
        return Query(content=query_dict_to_str(query), metadata=query)
    

    def replace_content(self, new_content: str) -> "Query":
        return Query(
            id=self.id,
            content=new_content,
            metadata=self.metadata,
        )
    

class EmbeddedQuery(Query):
    embedding: list[float]

    class Config:
        category = DataCategory.QUERIES
        
        
    
    