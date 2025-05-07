# backend/app/routers/cover_analysis.py

import base64
import json
from fastapi import APIRouter, HTTPException
from pathlib import Path
from typing import List

from backend.app.utils.cover_analysis.cover_analysis import analyze_cover

router = APIRouter()

@router.get("/cover_analysis_tab/{book_id}", response_model=List[dict])
def cover_analysis_tab_bookid(book_id: str):
    analysis_path = Path(f"backend/app/storage/covers/analysis/cover_analysis_{book_id}.json")
    image_path = Path(f"backend/app/storage/covers/{book_id}.png")

    if analysis_path.exists():
        try:
            with open(analysis_path, "r") as f:
                return json.load(f)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read cached analysis: {str(e)}")

    if not image_path.exists():
        raise HTTPException(status_code=404, detail=f"Cover for book ID '{book_id}' not found.")

    try:
        with open(image_path, "rb") as f:
            base64_image = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read cover image: {str(e)}")

    analysis = analyze_cover(base64_image)

    try:
        analysis_path.parent.mkdir(parents=True, exist_ok=True)
        with open(analysis_path, "w") as f:
            json.dump(analysis, f, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save analysis: {str(e)}")

    return analysis

