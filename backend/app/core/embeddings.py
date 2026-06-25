from sentence_transformers import SentenceTransformer
import numpy as np
from app.config import settings

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(settings.embed_model)
        self.dim = self.model.get_sentence_embedding_dimension()

    def encode(self, texts: list[str]) -> np.ndarray:
        emb = self.model.encode(
            texts, normalize_embeddings=True, convert_to_numpy=True
        )
        return emb.astype("float32")

embedder = Embedder()