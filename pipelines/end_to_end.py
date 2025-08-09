from zenml import pipeline

from .digital_data_etl import digital_data_etl
from .feature_engineering import feature_engineering
from steps.etl.create_indices import create_qdrant_indices_step


@pipeline
def end_to_end(collection_names: list[str], links: list[str], reflections: bool = False) -> str:
    data_pipeline_status = digital_data_etl(collection_names, links, reflections)
    embed_data_status = feature_engineering(data_pipeline_status)
    create_qdrant_indices_step(after=embed_data_status)
    return "End to end pipeline completed"