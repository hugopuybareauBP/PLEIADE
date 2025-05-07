# backend/app/utils/dashboard/genres.py

from langchain.schema.output_parser import StrOutputParser
from pathlib import Path

from backend.app.storage.storage import load_book_text, save_scores_as_json

from backend.app.utils.dashboard.llm import llm
from backend.app.utils.dashboard.prompts import genre_prompt_template

GENRES_CHART_DIR = Path("backend/app/storage/dashboards/genres_charts")

chain = genre_prompt_template | llm | StrOutputParser()

def get_genres_scores(synopsis) -> dict:
    content = chain.invoke({"text": synopsis})
    scores = {}
    for line in content.splitlines():
        if ":" in line:
            seg, pct = line.split(":", 1)
            scores[seg.strip()] = float(pct.strip().rstrip("%"))
    return scores

def genres_chart_pipeline(book_id: str):
    text = load_book_text(book_id)[:20000]

    genres_scores = get_genres_scores(text)
    print(f"[GENRES CHART GENERATOR] Genres repartition: {genres_scores}")

    save_scores_as_json(genres_scores, dir_path=GENRES_CHART_DIR, filename=f"genres_chart_{book_id}.json")

    return f"genres_chart_{book_id}.json"
