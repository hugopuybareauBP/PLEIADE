# backend/test/preprocessing/preprocessing_2.py

import re
from typing import List
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize

def remove_toc(text: str) -> str:
    toc_match = re.search(r"(table of contents|contents|toc)", text, re.IGNORECASE)

    if toc_match:
        print("TOC keyword detected")
        # Try to find first chapter after TOC
        chapter_match = re.search(r'(chapter\s+\d+|chapter\s+[ivxlc]+)', text[toc_match.end():], re.IGNORECASE)
        if chapter_match:
            cutoff = toc_match.end() + chapter_match.start()
            return text[cutoff:]
    return text

def detect_chapter_boundaries(text: str) -> List[str]:
    # Chapter 1, CHAPTER I, 1. Introduction, etc.
    pattern = re.compile(r'(?=(^((chapter|ch)\s+\d+|chapter\s+[ivxlc]+|^\d+\.\s+[A-Z])))(?=\s)', re.IGNORECASE | re.MULTILINE)
    matches = list(pattern.finditer(text))

    if len(matches) < 2:
        return []

    print(f"{len(matches)} chapter-like headings detected.")
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

    print("No chapters detected — fallback to sentence-based chunking.")
    return fallback_chunking(text, fallback_chunk_size)

if __name__ == "__main__":
    file_path = "backend/test/data/alice_in_wonderland.txt"
    with open(file_path, 'r') as file:
        text = file.read()
    chunks = split_into_chapters(text)
    print(f"\n=== Result: {len(chunks)} chunks ===\n")
    for i, chunk in enumerate(chunks[:2]):
        print(f"\n--- Chunk {i+1} ---\n")
        print(chunk[:1000])  # preview
        print("\n...\n")