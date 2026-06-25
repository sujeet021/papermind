import re
from app.config import settings

def chunk_text(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    size, overlap = settings.chunk_size, settings.chunk_overlap
    words, chunks, i = text.split(" "), [], 0
    while i < len(words):
        chunk = " ".join(words[i:i + size])
        if chunk:
            chunks.append(chunk)
        i += size - overlap
    return chunks