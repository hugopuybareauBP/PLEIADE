# backend/app/main.py

import uvicorn
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.routers import upload # UploadPage
from backend.app.routers import book_details # BookDetailsPage
from backend.app.routers import chat_stream # ChatStreamPage

app = FastAPI(
    title="My Book Analyzer",
    description="A simple API to analyze manuscripts (upload, chapter split, stats, etc.)",
    debug=True
)

covers_path = os.path.join("backend", "app", "storage", "covers")
app.mount("/covers", StaticFiles(directory=covers_path), name="covers")

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
app.include_router(book_details.router)
app.include_router(chat_stream.router, prefix="/chat")

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
