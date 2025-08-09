import os
import argparse
import opik
from loguru import logger
import openai

from gallery_recommender import settings
from gallery_recommender.infrastructure.opik_utils import configure_opik
from gallery_recommender.application.rag import ContextRetriever
from gallery_recommender.domain.embedded_cleaned_data import EmbeddedExhibitionDocument
from gallery_recommender.application.utils import misc
from gallery_recommender.model.inference import InferenceExecutor, ChatGPTInference

def main():
    configure_opik()
    openai.api_key = os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY

    parser = argparse.ArgumentParser(
        description="Custom RAG+ChatGPT run: retrieve k docs with optional filters, then ask ChatGPT"
    )
    parser.add_argument(
        "--query", "-q", required=True, help="Your free-form user query"
    )
    parser.add_argument(
        "--k", "-k", type=int, default=3, help="How many context docs to retrieve"
    )
    parser.add_argument(
        "--filter",
        "-f",
        nargs=2,
        action="append",
        metavar=("FIELD", "VALUE"),
        help="Metadata filter to apply (can repeat), e.g. `-f area ROPPONGI`",
    )
    args = parser.parse_args()

    # build filters dict or None
    filters = {field: value for field, value in (args.filter or [])}

    # 1) Retrieval
    retriever = ContextRetriever(mock=False)
    docs = retriever.search(args.query, k=args.k, filters=filters)

    logger.info(f"Retrieved {len(docs)} context docs")

    # 2) Build context string
    context = EmbeddedExhibitionDocument.to_context(docs)

    # 3) ChatGPT inference
    llm = ChatGPTInference(model_id=settings.OPENAI_MODEL_ID, api_key=settings.OPENAI_API_KEY, query=args.query)
    executor = InferenceExecutor(llm, args.query, context)
    answer = executor.execute()

    # 4) Show
    print("\n===== 🍭 RAG+ChatGPT ANSWER =====\n")
    print(answer)
    print("\n=================================\n")

if __name__ == "__main__":
    main()