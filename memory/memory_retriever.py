"""
memory_retriever.py
"""

from memory.embedding_model import EmbeddingModel
from memory.chroma_manager import ChromaManager

from memory.similarity_filter import SimilarityFilter
from memory.retrieval_ranker import RetrievalRanker


class MemoryRetriever:

    def __init__(self):

        self.embedding = EmbeddingModel()

        self.db = ChromaManager()

        self.filter = SimilarityFilter()

        self.ranker = RetrievalRanker()

    # ------------------------------------

    def retrieve(

        self,

        episode,

        top_k=5

    ):

        collection = self.db.get_collection()

        query_embedding = self.embedding.embed(

            episode

        )

        results = collection.query(

            query_embeddings=[query_embedding],

            n_results=top_k,

            include=[

                "documents",

                "metadatas",

                "distances"

            ]

        )

        filtered = self.filter.filter(

            results

        )

        ranked = self.ranker.rank(

            filtered

        )

        return ranked