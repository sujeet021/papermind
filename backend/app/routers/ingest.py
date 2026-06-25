from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
from app.utils.loaders import load_bytes
from app.core.chunker import chunk_text
from app.core.vectorstore import store
from app.models.schemas import IngestResponse

router = APIRouter(prefix="/api", tags=["ingest"])

@router.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...)):
    data = await file.read()
    text = load_bytes(file.filename, data)
    if not text.strip():
        raise HTTPException(400, "No extractable text found.")
    chunks = chunk_text(text)
    doc_id = str(uuid.uuid4())[:8]
    store.add(chunks, doc_id)
    return IngestResponse(doc_id=doc_id, chunks=len(chunks), filename=file.filename)