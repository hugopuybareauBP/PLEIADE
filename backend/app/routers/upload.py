# backend/app/routers/upload.py

import re
import logging
import datetime
import secrets
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

from fastapi import APIRouter, File, UploadFile, HTTPException

from backend.app.storage.storage import save_book, load_books, save_book_details
from backend.app.utils.preprocessing import preprocessing_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/books")
def get_books():
    logger.info("[get_books] Fetching all books.")
    return load_books()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

        logger.info(f"[upload_file] Received file upload: {file.filename}")

        try:
            content = await file.read()
            text = content.decode("utf-8", errors="replace")

            chunks = preprocessing_pipeline(text)

            logger.info(f"[upload_file] File '{file.filename}' processed successfully.")

        except Exception as e:
            logger.exception(f"[upload_file] Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        
        book_id = secrets.token_hex(4)
        book_data = {
            "id": book_id,
            "title": file.filename.replace(".txt", ""),
            "text": text,
            "cover": "",
            "author": "",
            "uploadDate": datetime.datetime.now().isoformat(),
            "progress": 50,
            "chunks": [
                {
                    "chunk_id": i,
                    "chunk_text": chunks[i]
                }
                for i in range(len(chunks))
            ]
        }
        save_book(book_data)
        logger.info(f"[upload_file] Book data saved with ID: {book_id}")

        default_details = {}   
        save_book_details(book_id, default_details)
        logger.info(f"[upload_file] Iinitiated detail instance with : {book_id}")
        
        return {"id": book_id}

