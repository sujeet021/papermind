from app.core.vectorstore import store
from app.core.intent import intent_clf
from app.core.extractor import extract
from app.core.llm import generate
from app.config import settings

SYSTEM = (
    "You are PaperMind, a precise document assistant. Answer ONLY from the "
    "provided context. If the context is insufficient, say 'I don't have "
    "enough information in the document to answer that.' Never invent facts."
)

def _format_ctx(hits):
    return "\n\n".join(f"[{i+1}] {h['text']}" for i, h in enumerate(hits))

def answer(question: str, mode: str, top_k: int | None):
    k = top_k or settings.top_k
    intent = intent_clf.classify(question) if mode == "auto" else mode
    hits = store.search(question, k)

    grounded = bool(hits) and hits[0]["score"] >= settings.score_threshold
    if not grounded:
        return {
            "answer": "I don't have enough information in the document to answer that.",
            "intent": intent, "sources": hits, "grounded": False,
        }

    ctx = _format_ctx(hits)

    if intent == "extract":
        data = extract(ctx)
        ans = "\n".join(f"{k}: {', '.join(v)}" for k, v in data.items()) or \
              "No structured fields found in the relevant context."
    elif intent == "summarize":
        ans = generate(f"Summarize the following context concisely:\n\n{ctx}", SYSTEM)
    else:  # qa
        ans = generate(f"Context:\n{ctx}\n\nQuestion: {question}", SYSTEM)

    return {"answer": ans, "intent": intent, "sources": hits, "grounded": True}