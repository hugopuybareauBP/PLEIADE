# backend/app/routers/summary.py

from ollama import chat 

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

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

def summarize_all_chunks(manuscript_obj: dict) -> dict:

    summarized_chunks = []

    for chunk_dict in manuscript_obj["chunk_list"]:
        chunk_id = chunk_dict["chunk_id"]
        chunk_text = chunk_dict[f"chunk_text"]
        print(f"[INFO] Summarizing chunk {chunk_id}...")
        summary = summarize_chunk_with_mistral(chunk_text, chunk_id)
        summarized_chunks.append(summary)

    return {
        "filename": manuscript_obj["filename"],
        "summaries": summarized_chunks
    }

class Chunk(BaseModel):
    chunk_id: int
    chunk_text: str

class ManuscriptPayload(BaseModel):
    filename: str
    full_text: str
    chunks: List[Chunk]

@router.post("/summarize")
async def summarize_manuscript(payload: ManuscriptPayload):
    try:
        manuscript_dict = payload.dict()
        result = summarize_all_chunks(manuscript_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))