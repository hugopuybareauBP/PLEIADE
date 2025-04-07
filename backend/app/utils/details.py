# backend/app/generation/details.py

import random as rd

from backend.app.generation.llm import build_chapter_breakdown, build_synopsis
from backend.app.generation.llm import build_ecommerce_desc, build_tweet
from backend.app.storage.storage import load_book_chunks, load_book_details

def generate_analysis_components(book_id):
    chunks = load_book_chunks(book_id)
    chapter_breakdown = build_chapter_breakdown(chunks)

    analysis = {
            "impact": {
                "strengths": [],
                "weaknesses": []
            },
            "characters": [],
            "chapters": chapter_breakdown 
        }
    
    return analysis

def generate_overview_components(book_id: str) -> dict:
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
    book_data = load_book_details(book_id)
    synopsis = book_data.get("analysis", {}).get("synopsis", "")
    print(synopsis)

    marketing = {
        "ecommerce": {
            "title": "Generated Title Placeholder",
            "description": build_ecommerce_desc(synopsis),
            "bullets": [],
            "closing": ""
            },
        "social_media": {
            "twitter": [
                {
                    "content" : build_tweet(synopsis),
                    "metrics" : {
                        "likes": rd.randit(0, 100),
                        "retweets": rd.randit(0, 100)
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



