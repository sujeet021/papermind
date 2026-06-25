import numpy as np
from app.core.embeddings import embedder

LABELS = {
    "qa": "answer a specific question about the document",
    "summarize": "summarize or give an overview of the document",
    "extract": "extract specific fields like dates, names, numbers, emails",
}

class IntentClassifier:
    def __init__(self):
        self.labels = list(LABELS.keys())
        self.protos = embedder.encode(list(LABELS.values()))

    def classify(self, q: str) -> str:
        v = embedder.encode([q])[0]
        sims = self.protos @ v
        return self.labels[int(np.argmax(sims))]

intent_clf = IntentClassifier()