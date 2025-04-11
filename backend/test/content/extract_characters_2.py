# backend/test/content/extract_characters_2.py

import time
import re

from collections import Counter, defaultdict

def extract_name_candidates(text: str): 
    return re.findall(r"\b(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b", text)

def normalize_name(name: str) -> str:
    return name.lower().strip().replace(" ", "_")

def get_top_characters_heuristic(text: str, top_n=5, min_len=3):
    raw_candidates = extract_name_candidates(text)
    
    # Filter out common false positives
    blacklist = {"Chapter", "Down", "Mouse", "Soup", "Story", "Thenbill", "Longitude", "Latitude"}
    filtered = [c for c in raw_candidates if len(c) >= min_len and c not in blacklist]
    
    norm_counts = Counter(normalize_name(c) for c in filtered)
    top_characters = [name for name, _ in norm_counts.most_common(top_n)]
    return top_characters, norm_counts

if __name__ == '__main__':
    start = time.time()
    with open("backend/test/data/alice_in_wonderland.txt", "r") as file:
        book_text = file.read()
    
    top_characters, counts = get_top_characters_heuristic(book_text, top_n=5)

    print(f"Raw top characters: {top_characters}")
    print(f"Raw counts: {counts}")
    print(f"time taken: {time.time() - start:.2f} seconds")