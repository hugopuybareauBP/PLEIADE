# backend/app/generation/analysis.py

from backend.app.generation.llm import build_chapter_breakdown, build_synopsis
from backend.app.storage.storage import load_books, save_book_details

def generate_analysis_components(book_id):
    book = load_books(book_id)
    chunks = [c["chunk_text"] for c in book["chunks"]]

    chapter_breakdown = build_chapter_breakdown(chunks)
    synopsis = build_synopsis(chapter_breakdown)

    analysis = {
        "analysis": {
            "impact": {
                "strengths": [],
                "weaknesses": []
            },
            "characters": [],
            "chapters": chapter_breakdown 
        }
    }

    save_book_details(book_id, analysis)



