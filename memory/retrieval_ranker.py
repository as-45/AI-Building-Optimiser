"""
retrieval_ranker.py

Ranks retrieved memories.
"""


class RetrievalRanker:

    def rank(self, episodes):

        episodes.sort(

            key=lambda x: x["distance"]

        )

        return episodes