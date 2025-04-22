# backend/app/utils/details.py

import random as rd

# Overview imports
from backend.app.utils.details.llm import build_synopsis, build_time_period, build_genres, build_tone, build_keywords, build_comparison
from backend.app.utils.details.key_data import build_key_data
from backend.app.utils.details.thema_code import thema_code_pipeline
from backend.app.utils.details.parsers import parse_keywords
# Analysis imports
from backend.app.utils.details.llm import build_impact_analysis, build_chapter_breakdown
from backend.app.utils.details.profile_generation import profile_generation_pipeline
from backend.app.utils.details.location_generation import location_note_pipeline
# Marketing imports
from backend.app.utils.details.llm import build_ecommerce_description, build_tweet
from backend.app.utils.details.parsers import parse_ecommerce
# Global imports
from backend.app.utils.details.parsers import parse_model_json_response

# Storage imports
from backend.app.storage.storage import load_book_chunks, load_book_details, load_book_text, load_book_title, load_book_pages

def generate_analysis_components(book_id):
    print(f"[GENERATE_ANALYSIS_COMPONENTS] Generating analysis for book {book_id}...")
    chunks = load_book_chunks(book_id)
    chapter_breakdown = build_chapter_breakdown(chunks)

    analysis = {
            "impact": parse_model_json_response(build_impact_analysis(chapter_breakdown)),
            "characters": profile_generation_pipeline(chapter_breakdown),
            "locations": location_note_pipeline(chapter_breakdown),
            "chapters": chapter_breakdown 
        }
    
    return analysis

def generate_overview_components(book_id: str) -> dict:
    print(f"[GENERATE_OVERVIEW_COMPONENTS] Generating overview for book {book_id}...")
    book_data = load_book_details(book_id)
    chapter_breakdown = book_data.get("analysis", {}).get("chapters", "")
    title = load_book_title(book_id)
    pages = load_book_pages(book_id)
    synopsis = build_synopsis(chapter_breakdown, title)
    text = load_book_text(book_id)
    keywords = parse_keywords(build_keywords(synopsis, chapter_breakdown))

    overview = {
        "synopsis": synopsis,
        "keyData": build_key_data(text, chapter_breakdown, pages),
        "contentAnalysis": {
            "timePeriod": build_time_period(synopsis, chapter_breakdown),
            "genres": build_genres(synopsis, chapter_breakdown),
            "tone": build_tone(synopsis, chapter_breakdown),
            "keywords": keywords,
        },
        "classification": {
            "primaryThema": thema_code_pipeline(synopsis),
            "secondaryThema": [
                {"code": "UBJ", "label": "Impact of AI on social connections"},
                {"code": "KJM", "label": "AI in business strategy"},
                {"code": "PDR", "label": "Societal implications"}
            ],
            "qualifiers": [
                "4SP (For professional/vocational reference)",
                "4G (Research & development)"
            ]
        },
        "comparison" : parse_model_json_response(build_comparison(synopsis, keywords))
    }

    return overview

def generate_marketing_components(book_id):
    print(f"[GENERATE_MARKETING_COMPONENTS] Generating marketing for book {book_id}...")
    book_data = load_book_details(book_id)
    synopsis = book_data.get("overview", {}).get("synopsis", "")
    title = load_book_title(book_id)

    marketing = {
        "ecommerce": parse_ecommerce(build_ecommerce_description(synopsis, title)),
        "social": {
            "twitter": [
                {
                    "content" : build_tweet(synopsis),
                    "metrics" : {
                        "likes": rd.randint(0, 100),
                        "retweets": rd.randint(0, 100)
                    }
                },
                {
                    "content" : build_tweet(synopsis),
                    "metrics" : {
                        "likes": rd.randint(0, 100),
                        "retweets": rd.randint(0, 100)
                    }
                }
            ],
            "instagram": [
                {
                    "image" : "",
                    "content" : "to generate",
                    "metrics": {
                        "likes": rd.randint(0, 100),
                        "comments": rd.randint(0, 100)
                    }
                }
            ],
            "tiktok": [
                {
                    "thumbnail" : "to generate",
                    "caption" : "to generate",
                    "metrics": {
                        "views": "",
                        "likes": ""
                    }
                }
            ]
        },
        "visuals": []
    }
    print(f"[GENERATE_MARKETING_COMPONENTS] Marketing components generated successfully.")

    return marketing



