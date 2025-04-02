# backend/app/routers/overview.py

import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter()
BOOK_DETAILS_DIR = Path("backend/app/storage/books")

@router.get("/books/{book_id}/overview")
def get_book_overview(book_id: str):
    file_path = BOOK_DETAILS_DIR / f"book_{book_id}.json"

    if not file_path.exists():
        raise HTTPException(status_code=401, detail="Book details not found")

    with open(file_path, "r", encoding="utf-8") as f:
        book_data = json.load(f)

    if "overview" not in book_data:
        raise HTTPException(status_code=402, detail="Overview section not found")

    return book_data["overview"]