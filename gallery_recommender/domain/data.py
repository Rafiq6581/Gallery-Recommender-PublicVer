from abc import ABC
import datetime
from pydantic import UUID4, Field

from .base import NoSQLBaseData
from .types import DataCategory


class Data(NoSQLBaseData, ABC):
    name: str
    

class GalleryData(Data):
    # gallery_id: UUID4 
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

    class Settings:
        name = DataCategory.GALLERY


class ExhibitionData(Data):
    # exhibition_id: UUID4 = Field(alias="exhibition_id")
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
    latitude: float
    longitude: float

    class Settings:
        name = DataCategory.EXHIBITION


class UserData(Data):
    user_id: UUID4 = Field(alias="user_id")

    class Settings:
        name = DataCategory.USER


class PromptData(Data):
    prompt_id: UUID4 = Field(alias="prompt_id")

    class Settings:
        name = DataCategory.PROMPT

class QueryData(Data):
    query_id: UUID4 = Field(alias="query_id")

    class Settings:
        name = DataCategory.QUERIES


class ReflectionData(Data):
    class Settings:
        name = DataCategory.REFLECTION