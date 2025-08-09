from loguru import logger 
from typing_extensions import Annotated
from zenml import step

from gallery_recommender.domain.base import VectorBaseData
from gallery_recommender.application import utils


@step
def load_to_vector_db(
    data: Annotated[list, "data"]    
) -> Annotated[bool, "sucessful"]:
    logger.info(f"Loading {len(data)} data to vector database")

    grouped_data = VectorBaseData.group_by_class(data)
    for data_class, data_list in grouped_data.items():
        logger.info(f"Loading documents into {data_class.get_collection_name()}")
        for documents_batch in utils.misc.batch(data_list, size=4):
            try:
                data_class.bulk_insert(documents_batch)
            except Exception:
                logger.error(f"Failed to insert data into {data_class.get_collection_name()}")

                return False
            
    return True