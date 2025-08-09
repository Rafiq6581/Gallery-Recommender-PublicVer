from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from gallery_recommender.domain.cleaned_data import (
    CleanedData,
    CleanedExhibitionData,  
    CleanedReflectionData,
)

from gallery_recommender.domain.data import (
    Data,
    ExhibitionData,
    ReflectionData,
)


from .operations.clean_data import clean_text


DataT = TypeVar("DataT", bound=Data)
CleanedDataT = TypeVar("CleanedDataT", bound=CleanedData)


class CleaningDataHandler(ABC, Generic[DataT, CleanedDataT]):
    @abstractmethod
    def clean(self, data: DataT) -> CleanedDataT:
        pass


class ExhibitionCleaningHandler(CleaningDataHandler):
    def clean(self, data_model: ExhibitionData) -> CleanedExhibitionData:
        return CleanedExhibitionData(
            area=data_model.area,
            id=data_model.id,
            name=data_model.name,
            name_japanese=data_model.name_japanese,
            name_english=data_model.name_english,
            description=clean_text(data_model.description),
            description_japanese=clean_text(data_model.description_japanese),
            description_english=clean_text(data_model.description_english),
            artist=data_model.artist,
            exhibition_image_url=data_model.exhibition_image_url,
            exhibition_start_date=data_model.exhibition_start_date,
            exhibition_end_date=data_model.exhibition_end_date,
            exhibition_start_date_ts=data_model.exhibition_start_date_ts,
            exhibition_end_date_ts=data_model.exhibition_end_date_ts,
            gallery_id=data_model.gallery_id,
        )
    

class ReflectionCleaningHandler(CleaningDataHandler[ReflectionData, CleanedReflectionData]):
    def clean(self, data_model: ReflectionData) -> CleanedReflectionData:
        return CleanedReflectionData(
            id=data_model.id,
            content=clean_text(data_model.description),
        )
