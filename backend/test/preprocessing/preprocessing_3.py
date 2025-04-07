# backend/test/preprocessing/preprocessing_2.py

# c'est de la D parce que c'est sur les caractères et pas sur les mots en fait
import time
import re
from typing import List
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize
from ollama import chat
import json

def detect_toc_with_llm(text: str):
    sample = text[:10000]

    prompt = (
        f"You are a helpful assistant that cleans up books for analysis."
        f"Your task is to detect whether the following text contains a Table of Contents."
        f"If it does, respond ONLY with a JSON object like:"
        f'{{"start": <start_index>, "end": <end_index>}}'
        f"The start and end should be character positions of the TOC block in the original text."
        f"If there is no TOC, respond exactly with: NO_TOC\n\n"
        f"Here is the start of the book:\n"
        f"{sample}"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response["message"]["content"]
    
    if "NO_TOC" in content.upper():
        print("[INFO] LLM detected no TOC.")
        return None

    # Try to parse the response
    match = re.search(r'{"start":\s*(\d+),\s*"end":\s*(\d+)}', content)
    if match:
        start = int(match.group(1))
        end = int(match.group(2))
        print(f"[INFO] TOC detected by LLM from {start} to {end}.")
        return start, end

    print(f"[INFO] LLM response unclear or malformed: {content}")
    return None

def remove_toc(text: str) -> str:
    toc_bounds = detect_toc_with_llm(text)
    if toc_bounds:
        start, end = toc_bounds
        print(
            f"[TOC REMOVAL] Removing TOC based on LLM detection.\n"
            f"[TOC REMOVAL] We removed \n\n {text[start:end]}\n\n from the text."
            )
        return text[:start] + text[end:]
    return text

def detect_chapter_boundaries(text: str) -> List[str]:
    # Chapter 1, CHAPTER I, 1. Introduction, etc.
    pattern = re.compile(r'(?=(^((chapter|ch)\s+\d+|chapter\s+[ivxlc]+|^\d+\.\s+[A-Z])))(?=\s)', re.IGNORECASE | re.MULTILINE)
    matches = list(pattern.finditer(text))

    if len(matches) < 2:
        return []

    print(f"[INFO] {len(matches)} chapter-like headings detected.")
    chunks = []
    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i+1].start() if i + 1 < len(matches) else len(text)
        chunks.append(text[start:end].strip())
    return chunks

def fallback_chunking(text: str, max_words: int = 1000) -> List[str]:
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    word_count = 0

    for sentence in sentences:
        sentence_words = len(sentence.split())
        if word_count + sentence_words > max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            word_count = sentence_words
        else:
            current_chunk.append(sentence)
            word_count += sentence_words
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def split_into_chapters(text: str, fallback_chunk_size: int = 1000) -> List[str]:
    text = remove_toc(text)
    chapters = detect_chapter_boundaries(text)

    if chapters:
        return chapters

    print("[INFO] No chapters detected — fallback to sentence-based chunking.")
    return fallback_chunking(text, fallback_chunk_size)

if __name__ == "__main__":
    start = time.time()
    file_path = "backend/test/data/echoes.txt"
    with open(file_path, 'r') as file:
        text = file.read()
    remove_toc(text)
    print(f"[INFO] LLM detection took {time.time() - start:.2f} seconds")

    # chunks = split_into_chapters(text)
    # print(f"\n=== Result: {len(chunks)} chunks ===\n")
    # for i, chunk in enumerate(chunks[:2]):
    #     print(f"\n--- Chunk {i+1} ---\n")
    #     print(chunk[:1000])  # preview
    #     print("\n...\n")