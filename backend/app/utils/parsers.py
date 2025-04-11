# backend/app/utils/parsers.py

import json
import re

# Marketing parsers

def parse_ecommerce(raw: str) -> dict:
    try:
        print(f"[ECOMMERCE_PARSER] Raw text is JSON, returning direct load.")
        return json.loads(raw)
    except json.JSONDecodeError:
        print("[ECOMMERCE_PARSER] Raw text is not JSON, falling back to text parsing.")
        lines = raw.splitlines()
        description = []
        bullets = []
        closing = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if re.match(r"^[-•]", line): # we look for a bullet point
                bullets.append(re.sub(r"^[-•]\s*", "", line))
            else:
                description.append(line)

        # # Separate closing from description (last 1-2 lines)
        # if len(description) >= 2:
        #     closing = description[-1]
        #     description = description[:-1]

        return {
            "description": description,
            "bullets": bullets,
            "closing": []
        }
    
# Overview parsers

def parse_keywords(raw_output: str):
    # remove numbered list and commas
    cleaned = re.sub(r"\d+\.\s*", "", raw_output.strip())
    return [kw.strip().strip(",") for kw in cleaned.split(",") if kw.strip()]

def parse_numbered_line(raw_output: str) -> str:
    items = re.findall(r"\d+\.\s*([^,\n]+)", raw_output)
    cleaned = ", ".join(item.strip() for item in items if item.strip())
    return cleaned

def parse_comparison(raw_output):
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        results = []

        # Split on entry numbers (1., 2., etc.)
        entries = re.split(r"\n?\s*\d+\.\s*", raw_output.strip())

        for entry in entries:
            if not entry.strip():
                continue

            author, title, note = "", "", ""

            # === CASE 1: Oneliner format ===
            if "Short Note:" in entry:
                author_match = re.search(r"Author:\s*(.*?),\s*Title:", entry)
                title_match = re.search(r"Title:\s*\"?(.*?)\"?,\s*Short Note:", entry)
                note_match = re.search(r"Short Note:\s*(.*)", entry, re.DOTALL)
                
                if author_match and title_match and note_match:
                    author = author_match.group(1).strip()
                    title = title_match.group(1).strip().strip('"')
                    note = note_match.group(1).strip()

            # === CASE 2: Multiline format ===
            else:
                lines = entry.strip().splitlines()
                for line in lines:
                    if line.strip().lower().startswith("author:"):
                        author = line.split(":", 1)[1].strip()
                    elif line.strip().lower().startswith("title:"):
                        title = line.split(":", 1)[1].strip().strip('"')
                    elif line.strip().lower().startswith("note:"):
                        note = line.split(":", 1)[1].strip()
                    else:
                        # continuation of the note
                        note += " " + line.strip()

            if author and title:
                results.append({
                    "author": author,
                    "title": title,
                    "note": note.strip()
                })

        return json.dumps(results, indent=4)

# Analysis parsers

def parse_impact_analysis(raw_text: str) -> dict:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        print("[ANALYSIS_PARSER] Raw text is not JSON, falling back to text parsing.")

        strengths_match = re.search(r"\*\*Strengths:\*\*(.*?)(\*\*Weaknesses:\*\*|$)", raw_text, re.DOTALL)
        weaknesses_match = re.search(r"\*\*Weaknesses:\*\*(.*)", raw_text, re.DOTALL)

        strengths_raw = strengths_match.group(1).strip() if strengths_match else ""
        weaknesses_raw = weaknesses_match.group(1).strip() if weaknesses_match else ""

        strengths = [re.sub(r"^\d+\.\s*", "", line.strip()) for line in strengths_raw.split("\n") if line.strip()]
        weaknesses = [re.sub(r"^\d+\.\s*", "", line.strip()) for line in weaknesses_raw.split("\n") if line.strip()]

        return {
            "strengths": strengths,
            "weaknesses": weaknesses
        }