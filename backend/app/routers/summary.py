# backend/app/routers/summary.py

from ollama import chat 

import logging
import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, AsyncGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class Chunk(BaseModel):
    chunk_id: int
    chunk_text: str

class ManuscriptPayload(BaseModel):
    filename: str
    full_text: str
    chunks: List[Chunk]

def summarize_chunk_with_mistral(chunk_text: str, chunk_id: int) -> str:
    prompt = (
        f"Summarize the following book passage in 3 bullet points. "
        f"Focus on important events and characters.\n\n{chunk_text}"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "chunk_id": chunk_id,
        "summary": response["message"]["content"]
    }
    
@router.post("/summarize/stream")
async def summarize_stream(payload: ManuscriptPayload):
    async def generate_chunks() -> AsyncGenerator[str, None]:
        for chunk in payload.chunks:
            logger.info(f"[INFO] Summarizing chunk {chunk.chunk_id}...")
            summary = summarize_chunk_with_mistral(chunk.chunk_text, chunk.chunk_id)
            yield f"data: {json.dumps(summary)}\n\n"

    return StreamingResponse(generate_chunks(), media_type="text/event-stream")