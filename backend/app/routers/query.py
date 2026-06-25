from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.core.rag import answer

router = APIRouter(prefix="/api", tags=["query"])

@router.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    return answer(req.question, req.mode, req.top_k)