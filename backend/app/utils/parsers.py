# backend/app/utils/parsers.py

import json
import re

from typing import List

### GENERAL PARSERS ###

def parse_model_json_response(raw_output: str) -> dict | None:
    # Remove markdown code block wrappers like ```json
    cleaned = re.sub(r"^```(?:json|python)?|```$", "", raw_output.strip(), flags=re.IGNORECASE | re.MULTILINE).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        return None

### MARKETING PARSERS ###

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

        return {
            "description": description,
            "bullets": bullets,
            "closing": []
        }
    
### OVERVIEW PARSERS ###

def parse_thema_code_output(raw_output):
    match = re.match(r'\b([A-Z]{1,2})\b', raw_output.strip())
    return match.group(1) if match else None

### ANALYSIS PARSERS ###

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
    
def parse_character_candidates(raw_output: str) -> List[str]:
    lines = [line.strip("-• \n") for line in raw_output.splitlines() if line.strip()]
    candidates = []
    for line in lines:
        line = re.sub(r"^\d+[\.\)]\s*", "", line)  # remove leading numbers
        line = re.sub(r"\s*\(.*?\)", "", line).strip()  # remove parentheses
        if line:
            candidates.append(line)
    return candidates

def parse_top_characters(raw_output: str) -> List[str]:
    lines = [re.sub(r"^\d+[\.\)]\s*", "", line.strip("-• \n")) for line in raw_output.splitlines() if line.strip()]
    return lines