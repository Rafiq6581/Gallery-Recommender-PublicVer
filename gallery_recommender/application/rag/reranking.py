import opik 

from gallery_recommender.application.networks import CrossEncoderModelSingleton
from gallery_recommender.domain.embedded_cleaned_data import EmbeddedDocument
from gallery_recommender.domain.queries import Query

from .base import RAGStep
class Reranker(RAGStep):
    def __init__(self, mock: bool = False) -> None:
        super().__init__(mock=mock)

        self._model = CrossEncoderModelSingleton()

    @opik.track(name="Reranker.generate")
    def generate(self, query: Query, retrieved_docs: list[EmbeddedDocument], keep_top_k: int) -> list[EmbeddedDocument]:
        if self._mock:
            return retrieved_docs
        
        query_doc_tuples = [(query.content, doc.description) for doc in retrieved_docs]
        scores = self._model(query_doc_tuples)

        scores_query_doc_tuples = list(zip(scores, retrieved_docs))
        scores_query_doc_tuples.sort(key=lambda x: x[0], reverse=True)

        ranked_docs = [doc for _, doc in scores_query_doc_tuples[:keep_top_k]]

        return ranked_docs