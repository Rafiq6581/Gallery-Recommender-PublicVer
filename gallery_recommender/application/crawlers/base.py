from abc import ABC, abstractmethod

from gallery_recommender.domain.base import NoSQLBaseData


class BaseCrawler(ABC):
    model: type[NoSQLBaseData]
    
    @abstractmethod
    def extract(self, link: str, **kwargs) -> None: ...