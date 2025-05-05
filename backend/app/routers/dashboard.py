# backend/app/routers/dashboard.py

import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path

from backend.app.utils.dashboard.spider import spider_chart_pipeline

router = APIRouter()

SPIDER_CHART_DIR = Path("backend/app/storage/dashboards/spider_charts")

@router.get("/dashboard/spider-chart/{book_id}")
async def get_or_generate_spider_chart(book_id: str):
    filename = f"spider_chart_{book_id}.json"
    file_path = SPIDER_CHART_DIR / filename

    if not file_path.is_file():
        print(f"[DASHBOARD SPIDER CHART GENERATOR] Spider chart data for book_id={book_id} not found. Generating...")
        try:
            spider_chart_pipeline(book_id)
            if not file_path.is_file():
                raise Exception("Failed to generate spider chart data")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating spider chart: {str(e)}")

    with open(file_path, "r") as f:
        scores = json.load(f)

    return JSONResponse(content=scores)
