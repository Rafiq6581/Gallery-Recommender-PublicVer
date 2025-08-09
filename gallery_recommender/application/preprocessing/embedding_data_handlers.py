from loguru import logger
from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar, cast
from gallery_recommender.application.networks import EmbeddingModelSingleton
from gallery_recommender.domain.cleaned_data import CleanedExhibitionData, CleanedReflectionData, CleanedData
from gallery_recommender.domain.embedded_cleaned_data import (
    EmbeddedDocument,
    EmbeddedExhibitionDocument,
    EmbeddedReflectionDocument,
)
from gallery_recommender.domain.data import DataCategory
from gallery_recommender.domain.queries import Query, EmbeddedQuery

DocumentT = TypeVar("DocumentT", bound=CleanedData)
EmbeddedDocumentT = TypeVar("EmbeddedDocumentT", bound=EmbeddedDocument)


# Get our embedding model singleton (e.g. a sentence-transformer)
embedding_model = EmbeddingModelSingleton()


class EmbeddingDataHandler(ABC, Generic[DocumentT, EmbeddedDocumentT]):
    """
    Abstract base class for embedding data handlers.
    This class transforms a document (or batch of documents) into its embedded representation.
    """

    def embed(self, data_model: DocumentT) -> EmbeddedDocumentT:
        return self.embed_batch([data_model])[0]

    def embed_batch(self, data_models: List[DocumentT]) -> List[EmbeddedDocumentT]:
            logger.info(f"Embedding {len(data_models)} documents.")
            # Extract the text to embed from each document.
            # For exhibitions, we assume the text is in the 'description' attribute.
            logger.info(f"Data models: {data_models}")
            if data_models[0].get_category() == DataCategory.EXHIBITION:
                embedding_inputs = [getattr(dm, "description", "") for dm in data_models]
            else:
                embedding_inputs = [getattr(dm, "content", "") for dm in data_models]
            logger.info(f"Embedding inputs: {embedding_inputs}")
            embeddings = embedding_model(embedding_inputs, to_list=True)
            return [
                self.map_model(dm, cast(List[float], embeddings[i]))
                for i, dm in enumerate(data_models)
            ]

    @abstractmethod
    def map_model(self, data_model: DocumentT, embedding: list[float]) -> EmbeddedDocumentT:
        """
        Map a raw data model and its embedding into an embedded data model.
        Must be implemented by subclasses.
        """
        pass

class ExhibitionEmbeddingHandler(EmbeddingDataHandler):
    def map_model(self, data_model: CleanedExhibitionData, embedding: list[float]) -> EmbeddedExhibitionDocument:
        return EmbeddedExhibitionDocument(
            id=data_model.id,
            area=data_model.area,
            name=data_model.name,
            name_japanese=data_model.name_japanese,
            name_english=data_model.name_english,
            description=data_model.description,  # using the exhibition description as the text to embed
            description_japanese=data_model.description_japanese,
            description_english=data_model.description_english,
            artist=data_model.artist,
            exhibition_image_url=data_model.exhibition_image_url,
            exhibition_start_date=data_model.exhibition_start_date,
            exhibition_end_date=data_model.exhibition_end_date,
            exhibition_start_date_ts=data_model.exhibition_start_date_ts,
            exhibition_end_date_ts=data_model.exhibition_end_date_ts,
            gallery_id=data_model.gallery_id,
            embedding=embedding,
            metadata={
                "embedding_model_id": embedding_model.model_id,
                "embedding_size": embedding_model.embedding_size,
                "max_input_length": embedding_model.max_input_length,
            },
        )


class ReflectionEmbeddingHandler(EmbeddingDataHandler[CleanedReflectionData, EmbeddedReflectionDocument]):
    def embed_batch(self, data_models: List[CleanedReflectionData]) -> List[EmbeddedReflectionDocument]:
        # For reflections, we assume the text to embed is in the 'content' field.
        embedding_inputs = [data_model.content for data_model in data_models]
        embeddings = embedding_model(embedding_inputs, to_list=True)
        return [
            self.map_model(data_model, cast(List[float], embedding))
            for data_model, embedding in zip(data_models, embeddings)
        ]

    def map_model(self, data_model: CleanedReflectionData, embedding: List[float]) -> EmbeddedReflectionDocument:
        return EmbeddedReflectionDocument(
            id=data_model.id,
            name=data_model.name,
            content=data_model.content,
            # You can include additional reflection-specific fields here, e.g., reflection_date
            embedding=embedding,
            metadata={
                "embedding_model_id": embedding_model.model_id,
                "embedding_size": embedding_model.embedding_size,
                "max_input_length": embedding_model.max_input_length,
            },
        )
    

class QueryEmbeddingHandler(EmbeddingDataHandler):
    def map_model(self, data_model: Query, embedding: list[float]) -> EmbeddedQuery:
        return EmbeddedQuery(
            id=data_model.id,
            content=data_model.content,
            embedding=embedding,
            metadata={
                "embedding_model_id": embedding_model.model_id,
                "embedding_size": embedding_model.embedding_size,
                "max_input_length": embedding_model.max_input_length,
            },
        )