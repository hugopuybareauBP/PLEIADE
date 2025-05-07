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

def load_book_author(book_id: str) -> dict:
    with open(BOOKS_UPLOADPAGE_FILE, "r", encoding="utf-8") as f:
        books = json.load(f)

    for book in books:
        if book["id"] == book_id:
            return book.get("author", "")

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

def get_2nd_letter_prompt(primary_thema_code):
    file_path = "backend/app/storage/thema_codes/2nd_letter_prompts.json"
    try:
        with open(file_path, "r") as f:
            prompts = json.load(f)
        return prompts.get(primary_thema_code.strip().upper(), f"No prompt found for code '{primary_thema_code}'")
    except FileNotFoundError:
        return f"File '{file_path}' not found."
    except json.JSONDecodeError:
        return "Error reading JSON file. Please ensure it is properly formatted."
    
def get_3rd_letter_prompt(second_letter):
    file_path = "backend/app/storage/thema_codes/3rd_letter_prompts.json"
    try:
        with open(file_path, "r") as f:
            prompts = json.load(f)
        return prompts.get(second_letter.strip().upper(), f"No prompt found for 2nd letter '{second_letter}'")
    except FileNotFoundError:
        return f"File '{file_path}' not found."
    except json.JSONDecodeError:
        return "Error reading JSON file. Please ensure it is properly formatted."
    
def get_thema_code_desc(code_value):
    file_path = "backend/app/storage/thema_codes/thema_codes.json"
    try:
        with open(file_path, "r") as f:
            thema_json = json.load(f)
    except FileNotFoundError:
        return f"File '{file_path}' not found."
    except json.JSONDecodeError:
        return "Error reading JSON file. Please ensure it is properly formatted."
    codes = thema_json.get("CodeList", {}).get("ThemaCodes", {}).get("Code", [])
    
    for code_entry in codes:
        if code_entry.get("CodeValue") == code_value:
            return code_entry.get("CodeDescription")
    return None

def load_main_genre(book_id: str) -> str:
    path = STORAGE_PATH / f"book_{book_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Book file not found")

    with open(path, "r", encoding="utf-8") as f:
        book_data = json.load(f)

    try:
        genres_str = book_data["overview"]["contentAnalysis"]["genres"]
        genres = [g.strip() for g in genres_str.split(",")]
        return genres[0] if genres else "Unknown"
    except KeyError:
        raise HTTPException(status_code=422, detail="Genre information not found in book file")

# DASHBOARD METHODS

def save_scores_as_json(audience_scores: dict, dir_path: Path, filename: str, ):
    """Save the audience scores dictionary as a JSON file."""
    dir_path.mkdir(parents=True, exist_ok=True)
    output_path = dir_path / filename

    with open(output_path, "w") as f:
        json.dump(audience_scores, f, indent=4)

    print(f"[SPIDER CHART GENERATOR] Saved audience scores at: {output_path}")
