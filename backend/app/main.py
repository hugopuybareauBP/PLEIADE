# backend/app/main.py

import uvicorn
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers import upload # UploadPage

from backend.app.routers import overview, analysis_marketing # BookDetailsPage

app = FastAPI(
    title="My Book Analyzer",
    description="A simple API to analyze manuscripts (upload, chapter split, stats, etc.)"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS middleware
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(upload.router)
app.include_router(overview.router)
app.include_router(analysis_marketing.router)

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
