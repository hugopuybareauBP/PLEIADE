# backend/test/content/impact_analysis.py

import time
import json
import re 

from rich.console import Console
from rich.panel import Panel

from ollama import chat 

console = Console()

def build_impact_analysis(chapter_breakdown) -> str:
    print(f"[BUILD_IMPACT_ANALYSIS] Building impact analysis...")
    context = "\n".join([c["raw_output"] for c in chapter_breakdown])
    
    prompt = (
        f"You are a professional book analyst. Based on the chapter summaries below, write a list of strengths and weaknesses "
        f"for this book. Focus on writing style, structure, clarity, examples, and depth of content.\n\n"
        f"Do not reference chapters directly. Instead, extract high-level impressions.\n\n"
        f"Chapter summaries:\n{context}\n\n"
        f"Return two separate lists:\n"
        f"- Strengths (5 items max)\n"
        f"- Weaknesses (5 items max)\n\n"
        "Respond with a JSON object like this: {\"strengths\": [\"...\"], \"weaknesses\": [\"...\"]\n}"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

def parse_impact_analysis_output(raw_text: str) -> dict:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        print("[PARSER] Raw text is not JSON, falling back to text parsing.")

        strengths_match = re.search(r"\*\*Strengths:\*\*(.*?)(\*\*Weaknesses:\*\*|$)", raw_text, re.DOTALL)
        weaknesses_match = re.search(r"\*\*Weaknesses:\*\*(.*)", raw_text, re.DOTALL)

        strengths_raw = strengths_match.group(1).strip() if strengths_match else ""
        weaknesses_raw = weaknesses_match.group(1).strip() if weaknesses_match else ""

        strengths = [re.sub(r"^\d+\.\s*", "", line.strip()) for line in strengths_raw.split("\n") if line.strip()]
        weaknesses = [re.sub(r"^\d+\.\s*", "", line.strip()) for line in weaknesses_raw.split("\n") if line.strip()]

        return {
            "impact": {
                "strengths": strengths,
                "weaknesses": weaknesses
            } 
        }

if __name__ == "__main__":
    start = time.time()
    filepath = "backend/test/summarization/summaries/echoes_3.json"
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    console.print(Panel(f"[bold cyan] Generating impact analysis[/]"))
    impact_analysis= build_impact_analysis(data['summary'])

    console.print(Panel(f"[bold magenta]IMPACT ANALYSIS:\n{impact_analysis}[/]"))
    console.print(Panel(f"[bold green]Tile elapsed : {time.time()-start:.2f} seconds ![/]"))