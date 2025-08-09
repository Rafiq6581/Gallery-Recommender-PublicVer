from concurrent.futures import ThreadPoolExecutor, as_completed

from loguru import logger 
from typing_extensions import Annotated
from zenml import get_step_context, step

from gallery_recommender.domain.base.nosql import NoSQLBaseData
from gallery_recommender.domain.data import ExhibitionData, GalleryData, Data


@step
def query_data_warehouse() -> Annotated[list, "raw_data"]:
    """Query the data warehouse for all Gallery and Exhibition data that are not already present in the vector database"""

    data = []
    results = fetch_all_data()
    art_spaces = [data for query_result in results.values() for data in query_result]
    data.extend(art_spaces)
    
    step_context = get_step_context()
    step_context.add_output_metadata(output_name="raw_data", metadata=_get_metadata(data))

    return data


def fetch_all_data() -> dict[str, list[NoSQLBaseData]]:
    """Fetch all Exhibition data from the data warehouse that are not already present in the vector database"""
    with ThreadPoolExecutor() as executor:
        future_to_query = {
            executor.submit(__fetch_exhibition_data): "exhibitions",
        }

        results = {}
        for future in as_completed(future_to_query):
            query_name = future_to_query[future]
            try:
                results[query_name] = future.result()
            except Exception as e:
                logger.error(f"Error fetching {query_name}: {e}")
                results[query_name] = []
        
        return results

    
def __fetch_exhibition_data() -> list[ExhibitionData]:
    """Fetch all Exhibition data from the data warehouse that are not already present in the vector database"""

    # Get all exhibitions from the data warehouse
    try:
        exhibitions = ExhibitionData.bulk_find()
        logger.info(f"Found {len(exhibitions)} exhibitions in the data warehouse")
        return exhibitions
    except Exception as e:
        logger.error(f"Error fetching exhibitions: {e}")
        return []
    

def _get_metadata(data: list[GalleryData | ExhibitionData]) -> dict:
    metadata = {
        "num_data": len(data),
    }
    for data in data:
        collection = data.get_collection_name()
        if collection not in metadata:
            metadata[collection] = {}
        metadata[collection]["num_data"] = metadata[collection].get("num_data", 0) + 1

    return metadata