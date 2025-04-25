import datetime
import secrets
import tiktoken
import pdfplumber

from fastapi import APIRouter, UploadFile, HTTPException
from fastapi import File, Form
from typing import Optional

from backend.app.storage.storage import (
    save_book, load_books, save_book_details,
    save_cover_image, load_book_details
)
from backend.app.utils.preprocessing.preprocessing import preprocessing_pipeline

enc = tiktoken.get_encoding("cl100k_base")

router = APIRouter()

@router.get("/books")
def get_books():
    print("[get_books] Fetching all books.")
    books = load_books()

    for book in books:
        details = load_book_details(book["id"])
        book["hasDetails"] = bool(
            details
            and "analysis" in details
            and "overview" in details
            and "marketing" in details
        )

    return books


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    cover: Optional[UploadFile] = File(None)
):
    print(f"[upload_file] Received file upload: {file.filename}")

    try:
        pages = 0

        if file.filename.endswith(".pdf"):
            print("[upload_file] Detected PDF file. Extracting text...")
            with pdfplumber.open(file.file) as pdf:
                text = "\n".join([page.extract_text() or "" for page in pdf.pages])
                pages = len(pdf.pages)
        else:
            content = await file.read()
            text = content.decode("utf-8", errors="replace")
            pages = text.count("\n") // 30  # rough estimate for .txt

        chunks = preprocessing_pipeline(text)
        print(f"[upload_file] File '{file.filename}' processed successfully.")

    except Exception as e:
        print(f"[upload_file] Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    book_id = secrets.token_hex(4)
    # book_id = "demo" # For demo purposes, using a fixed ID
    cover_url = ""
    if cover:
        cover_bytes = await cover.read()
        cover_url = save_cover_image(book_id, cover_bytes)

    book_data = {
        "id": book_id,
        "title": title or file.filename.replace(".txt", "").replace(".pdf", ""),
        "cover": cover_url or "/covers/no_cover.png",
        "author": author or "Author Unknown",
        "uploadDate": datetime.datetime.now().isoformat(),
        "pages": pages,
        "chunks": [
            {
                "chunk_id": i,
                "chunk_text": chunks[i]
            }
            for i in range(len(chunks))
        ],
        "text": text
    }

    save_book(book_data)
    print(f"[upload_file] Book data saved with ID: {book_id}")

    default_details = {}
    save_book_details(book_id, default_details)
    print(f"[upload_file] Initiated detail instance with: {book_id}")

    return {"id": book_id}
