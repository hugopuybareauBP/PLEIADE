import json
import os

from pathlib import Path
from fastapi import HTTPException

BOOKS_UPLOADPAGE_FILE = Path("backend/app/storage/books_overview.json")
STORAGE_PATH = Path("backend/app/storage/books")

# UPLOAD PAGE METHODS
def load_books():
    if BOOKS_UPLOADPAGE_FILE.exists():
        with open(BOOKS_UPLOADPAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return ["Nope"]

def save_book(book_data):
    books = load_books()
    books.append(book_data)
    with open(BOOKS_UPLOADPAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4)

def save_cover_image(book_id: str, cover_bytes: bytes) -> str:
    folder = "backend/app/storage/covers"
    os.makedirs(folder, exist_ok=True)
    cover_path = os.path.join(folder, f"{book_id}.png")
    with open(cover_path, "wb") as f:
        f.write(cover_bytes)
    return f"/covers/{book_id}.png" # declared as a static file

# BOOK DETAILS METHODS

def load_book_chunks(book_id: str) -> dict:
    with open(BOOKS_UPLOADPAGE_FILE, "r", encoding="utf-8") as f:
        books = json.load(f)

    for book in books:
        if book["id"] == book_id:
            return book.get("chunks", [])

    raise ValueError(f"No book found with ID {book_id}")

def load_book_text(book_id: str) -> dict:
    with open(BOOKS_UPLOADPAGE_FILE, "r", encoding="utf-8") as f:
        books = json.load(f)

    for book in books:
        if book["id"] == book_id:
            return book.get("text", "")

    raise ValueError(f"No book found with ID {book_id}")

def load_book_title(book_id: str) -> dict:
    with open(BOOKS_UPLOADPAGE_FILE, "r", encoding="utf-8") as f:
        books = json.load(f)

    for book in books:
        if book["id"] == book_id:
            return book.get("title", "")

    raise ValueError(f"No book found with ID {book_id}")

def load_book_pages(book_id: str) -> dict:
    with open(BOOKS_UPLOADPAGE_FILE, "r", encoding="utf-8") as f:
        books = json.load(f)

    for book in books:
        if book["id"] == book_id:
            return book.get("pages", "")

    raise ValueError(f"No book found with ID {book_id}")
    
def save_book_details(book_id: str, book_data: dict): #override
    path = STORAGE_PATH / f"book_{book_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(book_data, f, indent=4, ensure_ascii=False)

def load_book_details(book_id: str) -> dict:
    path = STORAGE_PATH / f"book_{book_id}.json"
    if not path.exists():
        raise HTTPException(status_code=401, detail="Book details not found")
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def get_book_path(book_id: str) -> str:
    return os.path.join(STORAGE_PATH, f"book_{book_id}.json")

# BOOKS OVERVIEW METHODS

def get_2nd_letter_thema_code_prompt(primary_thema_code):
    file_path = "backend/app/storage/thema_codes/secondary_thema_prompts.json"
    try:
        with open(file_path, "r") as f:
            prompts = json.load(f)
        return prompts.get(primary_thema_code.strip().upper(), f"No prompt found for code '{primary_thema_code}'")
    except FileNotFoundError:
        return f"File '{file_path}' not found."
    except json.JSONDecodeError:
        return "Error reading JSON file. Please ensure it is properly formatted."
    
def get_thema_code_desc(thema_code):
    file_path = "backend/app/storage/thema_codes/thema_lookup.json"
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data.get(thema_code.strip().upper(), f"No text found for code '{thema_code}'")
    except FileNotFoundError:
        return f"File '{file_path}' not found."
    except json.JSONDecodeError:
        return "Error reading JSON file. Please ensure it is properly formatted."

