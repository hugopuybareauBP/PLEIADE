# backend/test/content/extract_characters_4.py

import os
import json
import re
import time

from typing import List
from openai import AzureOpenAI
from sentence_transformers import SentenceTransformer, util

import torch

# Azure OpenAI Configuration
api_version = "2024-12-01-preview"
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_INFERENCE_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_INFERENCE_ENDPOINT")
AZURE_OPENAI_MODEL_NAME = os.getenv("AZURE_OPENAI_INFERENCE_MODEL_NAME")

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=api_version,
)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_character_candidates_from_chunk(text: str) -> List[str]:
    prompt = (
        f"Extract the full names of fictional characters explicitly mentioned in this book excerpt.\n"
        f"Only include clearly named characters (no pronouns, vague roles, or invented names).\n"
        f"Return as a bullet list.\n\n"
        f"{text}"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional literary analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=2048
    )

    return response.choices[0].message.content

def parse_character_candidates(raw_output: str) -> List[str]:
    lines = [line.strip("-• \n") for line in raw_output.splitlines() if line.strip()]
    candidates = []
    for line in lines:
        line = re.sub(r"^\d+[\.\)]\s*", "", line)  # remove leading numbers
        line = re.sub(r"\s*\(.*?\)", "", line).strip()  # remove parentheses
        if line:
            candidates.append(line)
    return candidates

def get_all_character_candidates_from_book(book_chunks: List[str], chunk_group_size: int = 5) -> List[str]:
    all_candidates = []
    for i in range(0, len(book_chunks), chunk_group_size):
        grouped_text = "\n\n".join(book_chunks[i:i + chunk_group_size])
        print(f"🔍 Processing chunks {i}–{i + chunk_group_size - 1}")
        raw_output = get_character_candidates_from_chunk(grouped_text)
        candidates = parse_character_candidates(raw_output)
        all_candidates.extend(candidates)

    # Deduplicate while preserving order
    seen = set()
    return [x for x in all_candidates if not (x in seen or seen.add(x))]

def build_top_characters(unique_candidates: List[str], n: int = 10) -> str:
    prompt = (
        f"Here is a list of character names from a book:\n\n"
        + "\n".join(f"- {name}" for name in unique_candidates) +
        f"\n\nClean this list by:\n"
        f"- Merging duplicate names (e.g., 'The Hatter' and 'Mad Hatter')\n"
        f"- Removing generic or non-informative entries\n"
        f"- Returning at most {n} of the most important characters as a bullet list only.\n"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional book analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=1024
    )

    return response.choices[0].message.content

def parse_top_characters(raw_output: str) -> List[str]:
    lines = [re.sub(r"^\d+[\.\)]\s*", "", line.strip("-• \n")) for line in raw_output.splitlines() if line.strip()]
    return lines

def extract_relevant_chunks(chunks: List[str], character_name: str, max_chunks: int = 5) -> List[str]:
    chunk_embeddings = embedding_model.encode(chunks, convert_to_tensor=True)
    query_embedding = embedding_model.encode(character_name, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_embedding, chunk_embeddings)[0]
    top_results = torch.topk(cosine_scores, k=min(max_chunks, len(chunks)))
    return [chunks[idx] for idx in top_results.indices]

def generate_character_profile(character_name: str, context: str) -> str:
    prompt = (
        f"Write a concise character profile for {character_name} using only the information below.\n"
        f"Return it as a JSON object like this:\n"
        f'{{"character": "{character_name}", "description": "<context-based summary>"}}\n'
        f"---\n{context}\n---"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a literary analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1024
    )

    return response.choices[0].message.content

def parse_model_json_response(raw_output: str) -> dict | None:
    # Remove markdown code block wrappers like ```json
    cleaned = re.sub(r"^```(?:json|python)?|```$", "", raw_output.strip(), flags=re.IGNORECASE | re.MULTILINE).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        return None

if __name__ == "__main__":
    start = time.time()
    filepath = "backend/test/summarization/summaries/echoes_azure_1.json"
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    summaries = [summary["raw_output"] for summary in data["summary"]]
    unique_candidates = get_all_character_candidates_from_book(summaries)
    print(unique_candidates)
    top_characters = parse_top_characters(build_top_characters(unique_candidates))
    print(f"\n🎯 Character candidates: {top_characters}\n")

    for char in top_characters[:5]:  # Limit to 5 for testing
        print(f"🧠 Generating profile for {char}...\n")
        context = "\n\n".join(extract_relevant_chunks(summaries, char, max_chunks=3))
        print(parse_model_json_response(generate_character_profile(char, context)))
        print("\n" + "-" * 40 + "\n")

    print(f"✅ Total time elapsed: {time.time()-start:.2f} seconds")
