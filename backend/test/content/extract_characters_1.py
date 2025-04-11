# backend/test/content/extract_characters.py

import time
import json
import re 
import spacy

from collections import Counter, defaultdict

nlp = spacy.load("en_core_web_sm")

def extract_characters_candidates(text: str): 
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return names

def normalize_name(name: str) -> str:
    name = re.sub(r"[^\w\s]", "", name) # punct
    return name.lower().strip().replace("mr.", "").replace("ms.", "").replace("dr.", "").replace("prof.", "").replace("professor", "").replace("doctor", "").replace(" ", "_")

def merge_name_variants(counts: Counter):
    merged = defaultdict(int)
    full_names = [name for name in counts if " " in name or "_" in name]
    name_map = {}

    # normalize full names
    for name in full_names:
        canonical = normalize_name(name.replace("_", " "))
        name_map[name] = canonical
        merged[canonical] += counts[name]
    
    # merge partials
    for name in counts:
        norm = normalize_name(name)
        if name not in name_map:
            continue # already merged

        found = False
        for full_name in merged:
            if norm in full_name:
                merged[full_name] += counts[name]
                found = True
                break
        
        if not found:
            merged[norm] += counts[name]
    
    return Counter(dict(sorted(merged.items(), key=lambda x: x[1], reverse=True)))

def get_top_characters(book_text: str, top_n=5):
    raw_names = extract_characters_candidates(book_text)
    normalized = [normalize_name(name) for name in raw_names]
    counts = Counter(normalized)
    top_characters = [name for name, _ in counts.most_common(top_n)]
    return top_characters, counts

def extract_character_context(chunks: list[str], top_characters: list[str]):
    context = defaultdict(list)
    for chunk in chunks:
        for name in top_characters:
            if name in chunk.lower():
                context[name].append(chunk)
    return {name: "\n\n".join(passages) for name, passages in context.items()}

if __name__ == '__main__':
    start = time.time()
    with open("backend/test/data/alice_in_wonderland.txt", "r") as file:
        book_text = file.read()
    
    top_characters, counts = get_top_characters(book_text, top_n=5)

    print(f"Raw top characters: {top_characters}")
    print(f"Raw counts: {counts}")
    print(f"time taken: {time.time() - start:.2f} seconds")

    merged = merge_name_variants(counts)
    print(f"Merged counts: {merged}")