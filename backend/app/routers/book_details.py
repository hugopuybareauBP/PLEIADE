# backend/app/routers/book_details.py

from fastapi import APIRouter, HTTPException
from backend.app.storage.storage import load_book_details, save_book_details
from backend.app.utils.details import (
    generate_overview_components,
    generate_analysis_components,
    generate_marketing_components
)

router = APIRouter()

@router.get("/books/{book_id}/details")
async def get_book_details(book_id: str):
    try: 
        book_data = load_book_details(book_id)

        if "analysis" not in book_data:
            print(f"[GET_BOOK_DETAILS] Generating analysis for book {book_id}...")
            book_data["analysis"] = generate_analysis_components(book_id)

        if "overview" not in book_data:
            print(f"[GET_BOOK_DETAILS] Generating overview for book {book_id}...")
            book_data["overview"] = generate_overview_components(book_id)

        if "marketing" not in book_data:
            print(f"[GET_BOOK_DETAILS] Generating marketing for book {book_id}...")
            book_data["marketing"] = generate_marketing_components(book_id)

        print(f"[GET_BOOK_DETAILS] Saving all sections for book {book_id}...")
        save_book_details(book_id, book_data)

        return book_data

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
