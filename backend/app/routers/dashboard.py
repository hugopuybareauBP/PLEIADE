# backend/app/routers/dashboard.py

import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path

from backend.app.utils.dashboard.target_reader import target_reader_chart_pipeline
from backend.app.utils.dashboard.genres import genres_chart_pipeline
from backend.app.utils.dashboard.style_dna import style_dna_pipeline_chunks, style_dna_pipeline_fulltext
from backend.app.storage.storage import load_main_genre

router = APIRouter()

TARGET_READER_CHART_DIR = Path("backend/app/storage/dashboards/target_reader_charts")
GENRES_CHART_DIR = Path("backend/app/storage/dashboards/genres_charts")
STYLE_DNA_DIR = Path("backend/app/storage/dashboards/style_dna")

@router.get("/dashboard/chart/{book_id}")
async def get_or_generate_spider_charts(book_id: str):
    target_reader_filename = f"target_reader_chart_{book_id}.json"
    genres_filename = f"genres_chart_{book_id}.json"
    style_dna_filename = f"style_dna_{book_id}.json"

    target_reader_path = TARGET_READER_CHART_DIR / target_reader_filename
    genres_path = GENRES_CHART_DIR / genres_filename
    style_dna_path = STYLE_DNA_DIR / style_dna_filename

    # Generate missing charts
    if not target_reader_path.is_file():
        print(f"[DASHBOARD] Target reader chart for book_id={book_id} not found. Generating...")
        try:
            target_reader_chart_pipeline(book_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating target reader chart: {str(e)}")

    if not genres_path.is_file():
        print(f"[DASHBOARD] Genre chart for book_id={book_id} not found. Generating...")
        try:
            genres_chart_pipeline(book_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating genres chart: {str(e)}")

    if not style_dna_path.is_file():
        print(f"[DASHBOARD] Style DNA chart for book_id={book_id} not found. Generating...")
        try:
            genre = load_main_genre(book_id)
            style_dna_pipeline_chunks(book_id, genre)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating style DNA chart: {str(e)}")

    # Read all charts
    try:
        with open(target_reader_path, "r") as f:
            target_reader_scores = json.load(f)

        with open(genres_path, "r") as f:
            genres_scores = json.load(f)

        with open(style_dna_path, "r") as f:
            style_dna_scores = json.load(f)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading chart files: {str(e)}")

    return JSONResponse(content={
        "target_reader": target_reader_scores,
        "genres": genres_scores,
        "style_dna": style_dna_scores
    })
