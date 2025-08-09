import concurrent.futures
import math
import opik
from loguru import logger 
from qdrant_client.models import MatchValue, Filter, FieldCondition, Range
import datetime

from gallery_recommender.application import utils
from gallery_recommender.application.preprocessing.dispatchers import EmbeddingDispatcher
from gallery_recommender.domain.embedded_cleaned_data import (
    EmbeddedDocument,
    EmbeddedExhibitionDocument, 
)

# TODO: Create Query and EmbeddedQuery classes
from gallery_recommender.domain.queries import Query, EmbeddedQuery

# TODO: Create Reranker class
from .reranking import Reranker 

now = datetime.datetime.now().timestamp()

class ContextRetriever:
    def __init__(self, mock: bool = False) -> None:
        self._reranker = Reranker(mock=mock)

    @opik.track(name="ContextRetriever.search")
    def search(
        self,
        query: dict,
        k: int = 3,
        filters: dict[str, str] | None = None,
    ) -> list: 
        query_model = Query.from_dict(query)
        
        # insert a metadata extractor if needed
        duration = getattr(query_model, "duration", None) or query.get("duration")
        k_documents = self._search(query_model, k, filters)

        logger.info(f"Retrieved {len(k_documents)} documents successfully")
        logger.info(f"Documents: {k_documents}")
        if len(k_documents) > 0:
            k_for_rerank = self._k_from_duration(duration)
            k_documents = self.rerank(query=query_model, retrieved_docs=k_documents, keep_top_k=k_for_rerank)
        else:
            k_documents = []

        return k_documents



    def _search(
        self,
        query: Query,
        k: int = 100,
        filters: dict[str, str | float] | None = None,
    ) -> list[EmbeddedDocument]:
        """
        Returns a list of lists of EmbeddedDocuments per category
        """
        assert k >= 1
        embedded_query: EmbeddedQuery = EmbeddingDispatcher.dispatch(query)

        # build a Qdrant `Filter` if any filters passed
        if filters:
            must = [
                FieldCondition(
                    key="exhibition_end_date_ts",
                    range=Range(gte=int(now)),
                )
            ]
            for key, val in filters.items():
                must.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=str(val)),
                    )
                )
            qdrant_filter = Filter(must=must)
        else:
            qdrant_filter = None

        def _search_data_category(
            data_category_odm: type[EmbeddedDocument], embedded_query: EmbeddedQuery
        ):
            return data_category_odm.search(
                query_vector=embedded_query.embedding,
                limit=k // 2,
                query_filter=qdrant_filter,
            )

        exhibition_documents = _search_data_category(EmbeddedExhibitionDocument, embedded_query)

        return exhibition_documents

    def rerank(self, query: str | Query, retrieved_docs: list[EmbeddedDocument], keep_top_k: int) -> list[EmbeddedDocument]:
        if isinstance(query, str):
            query = Query.from_str(query)

        reranked_documents = self._reranker.generate(query=query, retrieved_docs=retrieved_docs, keep_top_k=keep_top_k)

        logger.info(f"{len(reranked_documents)} documents reranked successfully")

        return reranked_documents
    

    def _k_from_duration(self, duration: str) -> int:
        hours = int(duration.split(" ")[0])
        k = math.floor((hours * 60) / 45)
        return max(1,k)