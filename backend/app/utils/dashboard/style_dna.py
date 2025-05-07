# backend/app/utils/dashboard/style_dna.py

from langchain.schema.output_parser import StrOutputParser
from pathlib import Path
from typing import List

from backend.app.storage.storage import load_book_text, save_scores_as_json
from backend.app.utils.dashboard.llm import llm
from backend.app.utils.dashboard.prompts import style_dna_prompt_template, emblematic_authors_by_genre
from backend.app.utils.details.parsers import parse_model_json_response

STYLE_DNA_DIR = Path("backend/app/storage/dashboards/style_dna")

chain = style_dna_prompt_template | llm | StrOutputParser()

def get_style_influences(text: str, genre: str) -> list[dict]:
    return parse_model_json_response(chain.invoke({"text": text, "genre": genre, "authors_list": ", ".join(emblematic_authors_by_genre[genre])}))

def style_dna_pipeline(book_id: str, genre: str):
    text = load_book_text(book_id)[:20000]

    style_scores = get_style_influences(text, genre)
    print(f"[STYLE DNA GENERATOR] Style repartition: {style_scores}")

    save_scores_as_json(style_scores, dir_path=STYLE_DNA_DIR, filename=f"style_dna_{book_id}.json")

    return f"style_dna_{book_id}.json"
