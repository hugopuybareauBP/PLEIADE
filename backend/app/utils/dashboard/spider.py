# backend/app/utils/dashboard/spider.py

import json
import matplotlib.pyplot as plt

from langchain.schema.output_parser import StrOutputParser
from pathlib import Path

from backend.app.storage.storage import load_book_details

from backend.app.utils.dashboard.llm import llm
from backend.app.utils.dashboard.prompts import spider_prompt_template

SPIDER_CHART_DIR = Path("backend/app/storage/dashboards/spider_charts")

chain = spider_prompt_template | llm | StrOutputParser()

def get_audience_scores(synopsis) -> dict:
    content = chain.invoke({"text": synopsis})
    scores = {}
    for line in content.splitlines():
        if ":" in line:
            seg, pct = line.split(":", 1)
            scores[seg.strip()] = float(pct.strip().rstrip("%"))
    return scores

def save_audience_scores_as_json(audience_scores: dict, filename: str):
    """Save the audience scores dictionary as a JSON file."""
    SPIDER_CHART_DIR.mkdir(parents=True, exist_ok=True)
    output_path = SPIDER_CHART_DIR / filename

    with open(output_path, "w") as f:
        json.dump(audience_scores, f, indent=4)

    print(f"[SPIDER CHART GENERATOR] Saved audience scores at: {output_path}")

def spider_chart_pipeline(book_id: str):
    """Full pipeline: load book -> generate audience scores -> save them as JSON."""
    book_data = load_book_details(book_id)
    synopsis = book_data.get("overview", {}).get("synopsis", "")

    audience_scores = get_audience_scores(synopsis)
    print(f"[SPIDER CHART GENERATOR] Audience scores: {audience_scores}")

    save_audience_scores_as_json(audience_scores, filename=f"spider_chart_{book_id}.json")

    return f"spider_chart_{book_id}.json"
