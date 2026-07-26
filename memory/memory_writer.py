"""
memory_writer.py

Stores episodes into ChromaDB.
"""

import json

from memory.chroma_manager import ChromaManager
from memory.embedding_model import EmbeddingModel


class MemoryWriter:

    def __init__(self):

        self.db = ChromaManager()

        self.embedding = EmbeddingModel()

    # --------------------------------------

    def store(self, episode):

        collection = self.db.get_collection()

        vector = self.embedding.embed(episode)

        document = self.embedding.build_text(episode)

        metadata = {

            "trigger": episode.trigger,

            "worst_zone": episode.worst_zone,

            "comfort": episode.average_comfort,

            "building_power": episode.average_building_power

        }

        collection.add(

            ids=[episode.episode_id],

            embeddings=[vector],

            documents=[document],

            metadatas=[metadata]

        )

        print(f"Stored Episode {episode.episode_id}")