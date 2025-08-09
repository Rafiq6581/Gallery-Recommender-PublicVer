from loguru import logger
from gallery_recommender.domain.embedded_cleaned_data import EmbeddedExhibitionDocument
from gallery_recommender.infrastructure.db.qdrant import QdrantDatabaseConnector


def initialize_indices():
    filterable_fields = list(EmbeddedExhibitionDocument.model_fields.keys())

    for field in filterable_fields:
        try:
            QdrantDatabaseConnector._instance.create_payload_index(
            collection_name=EmbeddedExhibitionDocument.Config.name,
            field_name=field,
            field_type="keyword" if field != "exhibition_start_date_ts" and field != "exhibition_end_date_ts" else "float",  # or "integer", "float" as needed
            )
            logger.info(f"Created index for field: {field}")
        except Exception as e:
            logger.warning(f"Index for {field} may already exist or failed to create: {e}")