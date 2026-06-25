import faiss, os, pickle
import numpy as np
from app.config import settings
from app.core.embeddings import embedder

class VectorStore:
    def __init__(self):
        self.dim = embedder.dim
        self.index = faiss.IndexFlatIP(self.dim)   # cosine (normalized)
        self.meta: list[dict] = []
        os.makedirs(settings.index_dir, exist_ok=True)
        self._load()

    def add(self, chunks: list[str], doc_id: str):
        vecs = embedder.encode(chunks)
        self.index.add(vecs)
        self.meta.extend({"text": c, "doc_id": doc_id} for c in chunks)
        self._save()

    def search(self, query: str, k: int):
        if self.index.ntotal == 0:
            return []
        q = embedder.encode([query])
        scores, idx = self.index.search(q, min(k, self.index.ntotal))
        return [
            {**self.meta[i], "score": float(s)}
            for s, i in zip(scores[0], idx[0]) if i != -1
        ]

    def _save(self):
        faiss.write_index(self.index, f"{settings.index_dir}/faiss.idx")
        with open(f"{settings.index_dir}/meta.pkl", "wb") as f:
            pickle.dump(self.meta, f)

    def _load(self):
        p = f"{settings.index_dir}/faiss.idx"
        if os.path.exists(p):
            self.index = faiss.read_index(p)
            with open(f"{settings.index_dir}/meta.pkl", "rb") as f:
                self.meta = pickle.load(f)

store = VectorStore()