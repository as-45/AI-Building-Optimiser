"""
chroma_manager.py

Handles the ChromaDB connection.
"""

import chromadb


class ChromaManager:

    def __init__(self):

        print("Initializing ChromaDB...")

        self.client = chromadb.PersistentClient(
            path="database/chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="building_episodes",
            metadata={
                "description": "Memory of previous building episodes"
            }
        )

        print("ChromaDB Ready.")

    # ----------------------------------------

    def get_collection(self):

        return self.collection