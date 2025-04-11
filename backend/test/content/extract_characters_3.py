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
        f"You are analyzing a book. Here is a list of character names that were mentioned:\n\n"
        + "\n".join(f"- {name}" for name in unique_candidates)
        + f"\n\nYour task is to:\n"
        f"- Identify and merge duplicate names (e.g. 'Mad Hatter' and 'The Hatter')\n"
        f"- Remove generic or repeated entries\n"
        f"- Select the {n} most important or relevant characters from this list\n"
        f"- Return **only** a bullet list of exactly {n} cleaned names\n\n"
        f"Do not include explanations, instance counts, or parentheticals. Just the list.\n"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    raw_output = response["message"]["content"]

    return raw_output

def parse_top_characters(raw_output: str) -> List[str]:
    important_start = re.search(r"(?i)(the\s+10\s+most\s+important.*?)\n", raw_output)

    if important_start:
        second_list = raw_output[important_start.end():]
    else:
        second_list = raw_output

    lines = [
        re.sub(r"^\d+[\.\)]\s*", "", line.strip("-• \n"))  # remove bullets and numbering
        for line in second_list.splitlines()
        if line.strip()
    ]

    return lines

def extract_relevant_chunks(chunks: list[str], character_name: str, max_chunks: int = 5) -> list[str]:
    name_lower = character_name.lower()
    relevant = [chunk for chunk in chunks if name_lower in chunk.lower()]
    return relevant[:max_chunks]

def generate_character_profile(character_name: str, context: str):
    prompt = (
        f"You are a literary analyst. Based on the context provided,"
        f"write a concise yet rich character profile for **{character_name}**.\n"
        f"Base your analysis only on the context provided.\n"
        f"---\n\n"
        f"{context}\n\n"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

if __name__ == "__main__":
    start = time.time()
    filepath = "backend/test/summarization/summaries/alice_vivid_prompt_2.json"
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    summaries = [summary["raw_output"] for summary in data["summary"]]
    unique_candidates = get_all_character_candidates_from_book(summaries)
    final_list = parse_top_characters(build_top_characters(unique_candidates))
    context = extract_relevant_chunks(summaries, final_list[0], max_chunks=3)
    print(f"Profile generation test: {generate_character_profile(final_list[0], context)}\n")
    print(f"Tile elapsed : {time.time()-start:.2f} seconds !")