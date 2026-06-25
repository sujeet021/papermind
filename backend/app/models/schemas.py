from pydantic import BaseModel
from typing import Literal, Optional

class IngestResponse(BaseModel):
    doc_id: str
    chunks: int
    filename: str

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = None
    mode: Literal["auto", "qa", "summarize", "extract"] = "auto"

class Source(BaseModel):
    text: str
    score: float
    doc_id: str

class QueryResponse(BaseModel):
    answer: str
    intent: str
    sources: list[Source]
    grounded: bool