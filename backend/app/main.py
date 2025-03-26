# backend/app/main.py

import uvicorn
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from backend.app.routers import summary, profile, spacy_stats, sentiment
from backend.app.routers import upload, summary

print(f"[DEBUG] {spacy_stats}")

app = FastAPI(
    title="My Book Analyzer",
    description="A simple API to analyze manuscripts (upload, chapter split, stats, etc.)"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS middleware
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(upload.router)
app.include_router(summary.router)

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
