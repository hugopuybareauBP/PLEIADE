import json
import os

from pathlib import Path

BOOKS_UPLOADPAGE_FILE = Path("backend/app/storage/books_overview.json")
STORAGE_PATH = Path("backend/app/storage/books")

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

def save_book_details(book_id: str, new_details: dict): #no override
    path = STORAGE_PATH / f"book_{book_id}.json"

    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            existing_details = json.load(f)
    else:
        existing_details = {}

    merged_details = {**existing_details, **new_details}

    with open(path, "w", encoding="utf-8") as f:
        json.dump(merged_details, f, indent=2, ensure_ascii=False)

def load_book_details(book_id: str) -> dict:
    path = STORAGE_PATH / f"book_{book_id}.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"Nope"}
    
def get_book_path(book_id: str) -> str:
    return os.path.join(STORAGE_PATH, f"book_{book_id}.json")