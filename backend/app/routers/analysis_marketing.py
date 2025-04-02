# backend/app/routers/analysis_marketing.py

import os
import json

from fastapi import APIRouter, HTTPException

from backend.app.storage.storage import load_book_details, save_book_details
from backend.app.generation.analysis import generate_analysis_components
# from backend.app.generation.marketing import generate_marketing_components

router = APIRouter()

@router.get("/books/{book_id}/analysis_marketing")
async def get_book_analysis_marketing(book_id: str):
    try:
        data = load_book_details(book_id)

        if "analysis" not in data:
            print(f"[INFO] Generating analysis for book {book_id}...")
            chunks = data.get("chunks", [])
            analysis = generate_analysis_components(chunks)
            data["analysis"] = analysis
            save_book_details(book_id, data)

        if "marketing" not in data:
            print(f"[INFO] Generating marketing for book {book_id}...")
            marketing = generate_marketing_components(data)
            data["marketing"] = marketing
            save_book_details(book_id, data)

        return {
            "analysis" : data["analysis"],
            "marketing" : data["marketing"]
        }

    except FileNotFoundError:
        raise HTTPException(status_code=405, detail="Book not found for analysis and marketing generation.")
    except Exception as e:
        raise HTTPException(status_code=405, detail=str(e))