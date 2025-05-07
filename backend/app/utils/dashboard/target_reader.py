# backend/app/utils/dashboard/spider.py

from langchain.schema.output_parser import StrOutputParser
from pathlib import Path

from backend.app.storage.storage import load_book_details, save_scores_as_json

from backend.app.utils.dashboard.llm import llm
from backend.app.utils.dashboard.prompts import target_reader_prompt_template

TARGET_READER_CHART_DIR = Path("backend/app/storage/dashboards/target_reader_charts")

chain = target_reader_prompt_template | llm | StrOutputParser()

def get_audience_scores(synopsis) -> dict:
    content = chain.invoke({"text": synopsis})
    scores = {}
    for line in content.splitlines():
        if ":" in line:
            seg, pct = line.split(":", 1)
            scores[seg.strip()] = float(pct.strip().rstrip("%"))
    return scores

def target_reader_chart_pipeline(book_id: str):
    book_data = load_book_details(book_id)
    synopsis = book_data.get("overview", {}).get("synopsis", "")

    audience_scores = get_audience_scores(synopsis)
    print(f"[TARGET READER CHART GENERATOR] Audience scores: {audience_scores}")

    save_scores_as_json(audience_scores, dir_path=TARGET_READER_CHART_DIR, filename=f"target_reader_chart_{book_id}.json")

    return f"target_reader_chart_{book_id}.json"
