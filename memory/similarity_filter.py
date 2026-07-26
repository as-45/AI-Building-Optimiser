"""
similarity_filter.py

Filters low-quality retrieval results.
"""


class SimilarityFilter:

    def __init__(self):

        # Lower distance = more similar
        self.max_distance = 0.6

    # -------------------------------------

    def filter(self, results):

        filtered = []

        ids = results["ids"][0]
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        for idx in range(len(ids)):

            if distances[idx] <= self.max_distance:

                filtered.append({

                    "id": ids[idx],

                    "document": docs[idx],

                    "metadata": metas[idx],

                    "distance": distances[idx]

                })

        return filtered