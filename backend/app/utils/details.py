# backend/app/utils/details.py

import random as rd

from backend.app.utils.llm import build_chapter_breakdown, build_synopsis, build_impact_analysis, parse_impact_analysis_output
from backend.app.utils.llm import build_ecommerce_desc, build_tweet
from backend.app.storage.storage import load_book_chunks, load_book_details

def generate_analysis_components(book_id):
    print(f"[GENERATE_ANALYSIS_COMPONENTS] Generating analysis for book {book_id}...")
    chunks = load_book_chunks(book_id)
    chapter_breakdown = build_chapter_breakdown(chunks)

    analysis = {
            "impact": parse_impact_analysis_output(build_impact_analysis(chapter_breakdown)),
            "characters": [],
            "chapters": chapter_breakdown 
        }
    
    print(analysis["impact"])
    
    return analysis

def generate_overview_components(book_id: str) -> dict:
    print(f"[GENERATE_OVERVIEW_COMPONENTS] Generating overview for book {book_id}...")
    book_data = load_book_details(book_id)
    chapter_breakdown = book_data.get("analysis", {}).get("chapters", "")
    synopsis = build_synopsis(chapter_breakdown)

    overview = {
        "synopsis": synopsis,
        "keyData": {
            "estimatedReadingTime": "",
            "wordCount": "",
            "pages": "",
            "chapters": f"{len(book_data.get('analysis', {}).get('chapters', []))} chapters",
            "mainCharacters": "",
            "keyLocations": ""
        },
        "contentAnalysis": {
            "timePeriod": "",
            "genres": "",
            "tone": "",
            "keywords": [
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                ""
            ]
        },
        "classification": {
            "primaryThema": "",
            "secondaryThema": [
                {"code": "UBJ", "label": "Impact of AI on social connections"},
                {"code": "KJM", "label": "AI in business strategy"},
                {"code": "PDR", "label": "Societal implications"}
            ],
            "qualifiers": [
                "4SP (For professional/vocational reference)",
                "4G (Research & development)"
            ]
        }
    }

    return overview

def generate_marketing_components(book_id):
    print(f"[GENERATE_MARKETING_COMPONENTS] Generating marketing for book {book_id}...")
    book_data = load_book_details(book_id)
    synopsis = book_data.get("analysis", {}).get("synopsis", "")

    marketing = {
        "ecommerce": {
            "title": "Generated Title Placeholder",
            "description": [build_ecommerce_desc(synopsis)],
            "bullets": [],
            "closing": ""
            },
        "social": {
            "twitter": [
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

    return marketing



