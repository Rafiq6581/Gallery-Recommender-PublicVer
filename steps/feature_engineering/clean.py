from typing_extensions import Annotated
from zenml import get_step_context, step

from gallery_recommender.application.preprocessing.dispatchers import CleaningDispatcher
from gallery_recommender.domain.cleaned_data import CleanedData


@step 
def clean_data(data: Annotated[list, "raw_data"]) -> Annotated[list, "cleaned_data"]:
    """Clean the data"""
    cleaned_data = []
    for data in data:
        cleaned_data.append(CleaningDispatcher.dispatch(data))

    step_context = get_step_context()
    step_context.add_output_metadata(output_name="cleaned_data", metadata=_get_metadata(cleaned_data))

    return cleaned_data


# this is similar to the _get_metadata function in query_data_warehouse.py
def _get_metadata(cleaned_data: list[CleanedData]) -> dict:
    metadata = {
        "num_cleaned_data": len(cleaned_data),
    }
    for data in cleaned_data:
        collection = data.get_collection_name()
        if collection not in metadata:
            metadata[collection] = {}
        metadata[collection]["num_data"] = metadata[collection].get("num_data", 0) + 1

    return metadata

