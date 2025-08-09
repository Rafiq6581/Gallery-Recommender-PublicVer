from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import UUID4, Field
import datetime

from .types import DataCategory
from .base import VectorBaseData  # your base vector document class


class EmbeddedDocument(VectorBaseData, ABC):
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    id: UUID4

    @abstractmethod
    def get_context_fields(self) -> Dict[str, Any]:
        """
        Return a dictionary of field names and values that should be included in the context.
        This must be implemented by each subclass.
        """
        pass

    @classmethod
    def to_context(cls, documents: List["EmbeddedDocument"]) -> str:
        context_lines = []
        for i, doc in enumerate(documents):
            context_lines.append(f"{cls.__name__} {i+1}:")
            fields = doc.get_context_fields()
            for key, value in fields.items():
                context_lines.append(f"{key}: {value}")
            context_lines.append("")  # blank line between documents
        return "\n".join(context_lines)


class EmbeddedExhibitionDocument(EmbeddedDocument):
    # Exhibition-specific fields
    area: str
    name: str
    description: str
    artist: str
    exhibition_image_url: str
    exhibition_start_date: datetime.datetime
    exhibition_end_date: datetime.datetime
    exhibition_start_date_ts: float
    exhibition_end_date_ts: float
    gallery_id: UUID4

    def get_context_fields(self) -> Dict[str, Any]:
        # Define the fields you want to include in the context for exhibitions.
        return {
            "Name": self.name,
            "Description": self.description,
            "Start Date": self.exhibition_start_date,
            "End Date": self.exhibition_end_date,
            "Gallery ID": self.gallery_id,
        }

    class Config:
        name = "embedded_exhibitions"
        category = DataCategory.EXHIBITION
        use_vector_index = True


class EmbeddedReflectionDocument(EmbeddedDocument):
    # Reflection-specific fields; note that reflections might not have a start date etc.
    content: str  # the reflection text
    reflection_date: Optional[datetime.datetime] = None

    def get_context_fields(self) -> Dict[str, Any]:
        fields = {"Name": self.name, "Reflection": self.content}
        if self.reflection_date:
            fields["Date"] = self.reflection_date
        return fields

    class Config:
        name = "embedded_reflections"
        category = DataCategory.REFLECTION
        use_vector_index = True