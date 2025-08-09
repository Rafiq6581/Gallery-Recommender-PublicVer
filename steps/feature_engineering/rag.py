from typing_extensions import Annotated
from loguru import logger
from zenml import get_step_context, step


from gallery_recommender.application.preprocessing.dispatchers import EmbeddingDispatcher
from gallery_recommender.domain.embedded_cleaned_data import EmbeddedDocument


@step
def embed_data(
    cleaned_documents: Annotated[list, "cleaned_documents"]
) -> Annotated[list, "embedded_documents"]:
    metadata = {"embedding": {}, "num_data": len(cleaned_documents)}

    embedded_documents = []
    for doc in cleaned_documents:
        # EmbeddingDispatcher.dispatch may return a single embedded document
        # or a list—adjust based on its implementation.
        result = EmbeddingDispatcher.dispatch(doc)
        logger.info(f"Embedding document: {doc}")
        if isinstance(result, list):
            embedded_documents.extend(result)
        else:
            embedded_documents.append(result)

    metadata["embedding"] = _add_embeddings_metadata(embedded_documents, metadata["embedding"])
    metadata["num_embedded_documents"] = len(embedded_documents)

    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="embedded_documents",
        metadata=metadata
    )

    return embedded_documents



def _add_embeddings_metadata(embedded_documents: list[EmbeddedDocument], metadata: dict) -> dict:
    for embedded_document in embedded_documents:
        category = embedded_document.get_category()
        if category not in metadata:
            metadata[category] = embedded_document.metadata

    return metadata