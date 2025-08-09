from zenml import step
from gallery_recommender.application.indexing import initialize_indices

@step(enable_cache=False)
def create_qdrant_indices_step() -> None:
    initialize_indices()