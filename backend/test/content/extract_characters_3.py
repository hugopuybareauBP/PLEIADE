# backend/test/content/extract_characters_3.py

import time
import json
import re

from ollama import chat
from typing import List
from collections import Counter

def get_character_candidates_from_chunk(text: str) -> List[str]:
    prompt = (
        "Your task is to extract the full names of **fictional characters** explicitly mentioned in the following book excerpt. "
        "Only list characters that are named clearly — do not invent or infer roles from pronouns or vague titles.\n\n"
        "Return the result as a bullet list.\n\n"
        f"{text}"
    )

    response = chat(model="mistral", messages=[{"role": "user", "content": prompt}])

    raw_output = response["message"]["content"]

    return raw_output

def parse_character_candidates(raw_output: str) -> List[str]:
    lines = [line.strip("-• \n") for line in raw_output.splitlines() if line.strip()]
    candidates = []

    for line in lines:
        # numbers
        line = re.sub(r"^\d+[\.\)]\s*", "", line)

        # ()
        line = re.sub(r"\s*\(.*?\)", "", line).strip()

        if line:
            candidates.append(line)

    return candidates

def get_all_character_candidates_from_book(book_chunks: List[str], chunk_group_size: int = 5) -> List[str]:

    all_candidates = []

    for i in range(0, len(book_chunks), chunk_group_size):
        grouped_text = "\n\n".join(book_chunks[i:i + chunk_group_size])
        print(f"🔍 Processing chunks {i}–{i + chunk_group_size - 1}")
        candidates = parse_character_candidates(get_character_candidates_from_chunk(grouped_text))
        all_candidates.extend(candidates)

    # duplicates
    seen = set()
    unique_candidates = []
    for name in all_candidates:
        if name not in seen:
            unique_candidates.append(name)
            seen.add(name)

    return unique_candidates

def build_top_characters(unique_candidates: List[str], n: int = 10):
    prompt = (
        f"Here is a list of characters mentioned in a book:\n"
        + "\n".join(f"- {name}" for name in unique_candidates)
        + f"Return a list of {n} characters, aggregate the one that seems to be the same, and remove duplicates."
        f" ONLY RETURN THE LIST OFT TOP {n}, WITHOUT ANY EXPLANATION.\n\n"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    raw_output = response["message"]["content"]

    return raw_output

if __name__ == "__main__":
    start = time.time()
    filepath = "backend/test/summarization/summaries/alice_vivid_prompt_2.json"
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    summaries = [summary["raw_output"] for summary in data["summary"]]
    unique_candidates = get_all_character_candidates_from_book(summaries)
    print(f"test : {build_top_characters(unique_candidates)}")
    print(f"Tile elapsed : {time.time()-start:.2f} seconds !")