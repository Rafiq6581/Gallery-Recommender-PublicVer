from typing import Optional

from loguru import logger
from tqdm import tqdm
from typing_extensions import Annotated
from zenml import get_step_context, step

from gallery_recommender.application.deleters.dispatcher import DeleterDispatcher


@step
def delete_data(collection_names: list[str]) -> Annotated[bool, "deleted_data"]:
    logger.info(f"Deleting {len(collection_names)} collections")
    metadata = {}
    dispatcher = DeleterDispatcher.build().register_mongodb().register_qdrant()
    try:
        successful_deletion = _delete_data(dispatcher, collection_names)
        metadata = _add_to_metadata(metadata, successful_deletion)
        step_context = get_step_context()
        step_context.add_output_metadata(
            output_name="deleted_data",
            metadata=metadata
        )
        return True
    except Exception as e:
        logger.error(f"Error deleting data: {e}")
        return False


def _delete_data(dispatcher: DeleterDispatcher, collection_names: list[str]) -> int:
    successful_deletion = 0
    for collection_name in collection_names:
        try:
            deleter = dispatcher.get_deleter(collection_name)
            logger.info(f"Deleting {collection_name} data")
            if deleter.delete_many(collection_name):
                successful_deletion += 1
        except Exception as e:
            logger.error(f"Error deleting {collection_name} data: {e}")

    return successful_deletion


def _add_to_metadata(metadata: dict, successful_deletion: int) -> dict:
    logger.info(f"Adding to metadata: {successful_deletion}")
    metadata["deleted"] = metadata.get("deleted", 0) + successful_deletion
    return metadata








