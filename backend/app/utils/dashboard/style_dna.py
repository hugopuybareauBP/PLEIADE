# backend/app/utils/dashboard/style_dna.py

from langchain.schema.output_parser import StrOutputParser
from pathlib import Path
from typing import List

from backend.app.storage.storage import load_book_text, save_scores_as_json, load_book_chunks
from backend.app.utils.dashboard.llm import llm
from backend.app.utils.dashboard.prompts import style_dna_prompt_template, emblematic_authors_by_genre
from backend.app.utils.details.parsers import parse_model_json_response

STYLE_DNA_DIR = Path("backend/app/storage/dashboards/style_dna")

chain = style_dna_prompt_template | llm | StrOutputParser()

def get_style_influences(text: str, genre: str) -> List[dict]:
    return parse_model_json_response(chain.invoke({"text": text, "genre": genre, "authors_list": ", ".join(emblematic_authors_by_genre[genre])}))

def style_dna_pipeline_fulltext(book_id: str, genre: str):
    text = load_book_text(book_id)[:20000]
    # print(text)
    style_scores = get_style_influences(text, genre)
    print(f"[STYLE DNA GENERATOR] Style repartition: {style_scores}")
    save_scores_as_json(style_scores, dir_path=STYLE_DNA_DIR, filename=f"style_dna_{book_id}.json")
    return f"style_dna_{book_id}.json"

def style_dna_pipeline_chunks(book_id: str, genre: str):
    chunks = load_book_chunks(book_id)
    if not chunks:
        raise ValueError(f"No chunks found for book {book_id}")
    chunk_snippets = [chunk["chunk_text"][:1000] for chunk in chunks if "chunk_text" in chunk] # Limit to 1000 characters per chunk
    text = "\n\n".join(chunk_snippets)[:20000]  # Limit total input at 20k like in fulltext
    # print(f"[STYLE DNA GENERATOR] Sample text from chunks:\n{text_sample[:1000]}...\n")
    style_scores = get_style_influences(text, genre)
    print(f"[STYLE DNA GENERATOR] Style repartition: {style_scores}")
    save_scores_as_json(style_scores, dir_path=STYLE_DNA_DIR, filename=f"style_dna_{book_id}.json")
    return f"style_dna_{book_id}.json"
