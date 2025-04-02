# backend/app/routers/analysis_marketing.py

import os
import json
from fastapi import APIRouter, HTTPException
from backend.app.storage.storage import get_book_path

router = APIRouter()

def load_book_json(book_id: str) -> dict:
    path = get_book_path(book_id)
    if not os.path.exists(path):
        raise HTTPException(status_code=403, detail="Book not found")
    with open(path, "r", encoding="utf-8") as f:
        return(json.load(f))

def save_book_json(book_id: str, data: dict):
    path = get_book_path(book_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@router.get("/books/{book_id}/analysis_marketing")
def get_book_analysis_marketing(book_id: str) -> dict:
    book_data = load_book_json(book_id)
    
    if "analysis" not in book_data:
            book_data["analysis"] = {
                "impact": {
                    "strengths": [],
                    "weaknesses": []
                },
                "characters": [],
                "chapters": []
            }
        # fill with the summarizer_3 hein

    if "marketing" not in book_data:
        book_data["marketing"] = {
            "ecommerce": {
                "title": "Coming Soon...",
                "description": [],
                "bullets": [],
                "closing": ""
            },
            "social": {
                "twitter": [],
                "instagram": [],
                "tiktok": []
            },
            "visuals": []
        }
        # fill with les codes de hier 

        save_book_json(book_id, book_data)

    return {
        "analysis": book_data["analysis"],
        "marketing": book_data["marketing"]
    }
