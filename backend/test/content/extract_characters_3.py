# backend/test/content/extract_characters_3.py

import time
import json
import re
import torch

from ollama import chat
from typing import List
from sentence_transformers import SentenceTransformer, util

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_character_candidates_from_chunk(text: str) -> List[str]:
    prompt = (
        "Your task is to extract the full names of **fictional characters** explicitly mentioned in the following book excerpt. "
        "Only list characters that are named clearly — do not invent or infer roles from pronouns or vague titles.\n\n"
        "Return the result as a bullet list.\n\n"
        f"{text}"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": 0.2,
        }
    )

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
        f"- Identify and merge duplicate names (e.g. 'Mad Hatter' and 'The Hatter').\n"
        f"- Remove generic or repeated entries.\n"
        f"- Select the most important or relevant characters from this list.\n"
        f"- Return **only** a bullet list of a maximum of {n} cleaned names\n\n"
        f"Do not include explanations, instance counts, or parentheticals. Just the list.\n"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": 0.2,
        }
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

# naive approach
# def extract_relevant_chunks(chunks: list[str], character_name: str, max_chunks: int = 5) -> list[str]:
#     name_lower = character_name.lower()
#     relevant = [chunk for chunk in chunks if name_lower in chunk.lower()]
#     return relevant[:max_chunks]

# cosine similarity approach
def extract_relevant_chunks(chunks: list[str], character_name: str, max_chunks: int = 5) -> list[str]:
    chunk_embeddings = embedding_model.encode(chunks, convert_to_tensor=True)
    # query is only character name
    query_embedding = embedding_model.encode(character_name, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_embedding, chunk_embeddings)[0]
    top_results = torch.topk(cosine_scores, k=min(max_chunks, len(chunks)))

    return [chunks[idx] for idx in top_results.indices]

# faiss approach??


# 7B has 8k token context window, protects against overloading
def truncate_context(chunks: list[str], max_tokens: int = 3000):
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
    total_tokens = 0
    selected_chunks = []

    for chunk in chunks:
        tokens = len(tokenizer.encode(chunk))
        if total_tokens + tokens > max_tokens:
            break
        selected_chunks.append(chunk)
        total_tokens += tokens

    return "\n\n".join(selected_chunks)

def generate_character_profile(character_name: str, context: str):
    prompt = (
        f"You are a literary analyst tasked with writing a factual and concise character profile.\n"
        f"Return your answer as a JSON list in the following format:\n"
        f'{{"character": "{character_name}", "description": "<concise profile based only on the context>"}}\n'
        f"Use **only** the information provided in the context below.\n"
        f"If the information is vague, keep your answer general and do not invent details.\n"
        f"---\n"
        f"{context}\n"
        f"---\n"
        f"Now write the character profile as JSON:"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": 0.2,
        }
    )

    return response["message"]["content"]

def parse_character_profile(raw_output: str):
    try:
        data = json.loads(raw_output)
        if not isinstance(data, dict):
            return None

        character = data.get("character", "").strip()
        description = data.get("description", "").strip()

        if character and description:
            return {"character": character, "description": description}
        return None

    except Exception as e:
        print(f"Parsing failed: {e}")
        return None
    
if __name__ == "__main__":
    start = time.time()
    filepath = "backend/test/summarization/summaries/echoes_4.json"
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    summaries = [summary["raw_output"] for summary in data["summary"]]
    unique_candidates = get_all_character_candidates_from_book(summaries)
    final_list = parse_top_characters(build_top_characters(unique_candidates))
    print(f"Character candidates: {final_list}\n")
    
    for char in final_list[:5] if len(final_list) > 5 else final_list:
        print(f"Profile generation test for {char}:\n\n")
        context = truncate_context(extract_relevant_chunks(summaries, char, max_chunks=3))
        context = context.replace(char, f"**{char}**")
        # print(f"Context:\n{context}\n")
        print(f"{generate_character_profile(char, context)}\n")
    print(f"Tile elapsed : {time.time()-start:.2f} seconds !")