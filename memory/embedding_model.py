"""
embedding_model.py
Creates embeddings for building episodes.
"""
from sentence_transformers import SentenceTransformer
from memory.episode_narrator import EpisodeNarrator


class EmbeddingModel:
    def __init__(self):
        print("Loading Nomic Embedding Model...")
        self.model = SentenceTransformer(
            "nomic-ai/nomic-embed-text-v1.5",
            trust_remote_code=True
        )
        self.narrator = EpisodeNarrator()
        print("Embedding Model Ready")

    # --------------------------------------
    def build_text(self, episode):
        return self.narrator.narrate(episode)

    # --------------------------------------
    def embed(self, episode):
        text = self.build_text(episode)
        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )
        return embedding.tolist()