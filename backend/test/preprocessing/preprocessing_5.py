# backend/test/preprocessing/preprocessing_5.py

import time
import tiktoken
import re

enc = tiktoken.get_encoding("cl100k_base")

def get_token_count(text: str) -> int:
    return len(enc.encode(text))

def remove_toc_using_chapter_density(text: str, max_gap_tokens: int = 100) -> str:
    chapter_pattern = re.compile(r'(chapter\s+\d+|chapter\s+[ivxlc]+)', re.IGNORECASE)
    matches = list(chapter_pattern.finditer(text))

    print(f"[REMOVE_TOC_USING_CHAPTER_DENSITY] Found {len(matches)} candidates.")

    for i in range(len(matches) - 1):
        current = matches[i]
        next_one = matches[i + 1]
        in_between = text[current.end():next_one.start()]
        gap_tokens = get_token_count(in_between)

        # still in the toc
        if gap_tokens <= max_gap_tokens:
            continue
        else:
            # first real chapter
            print(f"[REMOVE_TOC_USING_CHAPTER_DENSITY] First real chapter at position {current.start()}, gap to next: {gap_tokens} tokens")
            return text[current.start():]

    print("[REMOVE_TOC_USING_CHAPTER_DENSITY] Could not determine TOC end — returning original text.")
    return text

if __name__ == "__main__":
    start = time.time()
    file_path = "backend/test/data/moby_dick.txt"
    with open(file_path, 'r') as f:
        text = f.read()

    print(f"[TOC CLEANER] Original text token count: {get_token_count(text)}")
    print(f"Cleaning text...")
    text = remove_toc_using_chapter_density(text)
    print(f"[TOC CLEANER] Cleaned text token count: {get_token_count(text)}")
    print(f"[TOC CLEANER] First 1000 characters:\n{text[:1000]}")
    print(f"[TOC CLEANER] Time taken: {time.time() - start:.2f} seconds")


