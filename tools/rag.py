import argparse
from langchain.globals import set_verbose
from loguru import logger

from gallery_recommender.application.rag import ContextRetriever
from gallery_recommender.infrastructure.opik_utils import configure_opik


if __name__ == "__main__":
    configure_opik()
    set_verbose(True)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filter",
        nargs=2,
        action="append",
        metavar=("FIELD", "VALUE"),
        help="Metadata filter to apply, e.g. `--filter area ROPPONGI`",
    )
    args = parser.parse_args()

    query = """
        I wish to visit an art exhibition. Based on the following information, could you recommend me an art exhibition?
        * Art Knowledge Level: Intermediate
        * Reason for Gallery Visit: For inspiration
        * Time Available: 2 hours
        * Current Mood: Joyful
    """
    

    filters = {field: value for field, value in (args.filter or [])}

    retriever = ContextRetriever(mock=False)
    documents = retriever.search(query, k=9, filters=filters)

    logger.info("Retrieved documents:")
    for rank, document in enumerate(documents):
        logger.info(f"{rank + 1}: {document}")