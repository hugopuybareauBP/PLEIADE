# backend/app/utils/parsers.py

import json
import re

from typing import List

### GENERAL PARSERS ###

def parse_model_json_response(raw_output: str) -> dict | None:
    # Remove common markdown formatting (```json, etc.)
    cleaned = re.sub(r"^```(?:json|python)?|```$", "", raw_output.strip(), flags=re.IGNORECASE | re.MULTILINE).strip()

    # Attempt to fix concatenated dicts: turn `} , {` into a proper combined dict
    if "},\"" in cleaned and cleaned.count("{") == 1:
        cleaned = "{" + cleaned.replace("},\"", ",\"").lstrip("{")

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

def parse_keywords(raw_input: str) -> list[str]:
    return [item.strip().capitalize() for item in raw_input.split(",") if item.strip()]

### ANALYSIS PARSERS ###
    
def parse_candidates(raw_output: str) -> List[str]:
    lines = [line.strip("-• \n") for line in raw_output.splitlines() if line.strip()]
    candidates = []
    for line in lines:
        line = re.sub(r"^\d+[\.\)]\s*", "", line)  # remove leading numbers
        line = re.sub(r"\s*\(.*?\)", "", line).strip()  # remove parentheses
        if line:
            candidates.append(line)
    return candidates

def parse_top_candidates(raw_output: str) -> List[str]:
    lines = [re.sub(r"^\d+[\.\)]\s*", "", line.strip("-• \n")) for line in raw_output.splitlines() if line.strip()]
    return lines