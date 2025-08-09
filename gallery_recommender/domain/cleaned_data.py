from abc import ABC
import datetime
from pydantic import UUID4

from .base import VectorBaseData
from .types import DataCategory


class CleanedData(VectorBaseData, ABC):
    pass
    

class CleanedGalleryData(CleanedData):
    name: str
    name_japanese: str
    name_english: str
    description: str
    address_japanese: str
    address_english: str
    area: str
    gallery_image_url: str
    website: str
    hours: str
    latitude: float
    longitude: float
    phone_number: str

    class Config:
        name = "cleaned_gallery_data"
        category = DataCategory.GALLERY
        use_vector_index = False
    

class CleanedExhibitionData(CleanedData):
    name: str
    name_japanese: str
    name_english: str
    area: str
    description: str
    description_japanese: str
    description_english: str
    artist: str
    exhibition_image_url: str
    exhibition_start_date: datetime.datetime
    exhibition_end_date: datetime.datetime
    exhibition_start_date_ts: float
    exhibition_end_date_ts: float
    gallery_id: UUID4


    class Config:
        name = "cleaned_exhibition_data"
        category = DataCategory.EXHIBITION
        use_vector_index = False


class CleanedUserData(CleanedData):

    class Config:
        name = "cleaned_user_data"
        category = DataCategory.USER
        use_vector_index = False

class CleanedPromptData(CleanedData):

    class Config:
        name = "cleaned_prompt_data"
        category = DataCategory.PROMPT
        use_vector_index = False


class CleanedQueryData(CleanedData):

    class Config:
        name = "cleaned_query_data"
        category = DataCategory.QUERIES
        use_vector_index = False


class CleanedReflectionData(CleanedData):

    class Config:
        name = "cleaned_reflection_data"
        category = DataCategory.REFLECTION
        use_vector_index = False