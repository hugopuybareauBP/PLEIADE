# backend/test/preprocessing/preprocessing_4.py

import time
import re
import tiktoken

from ollama import chat

def get_first_n_tokens(text: str, n: int = 3000) -> str:
    enc = tiktoken.get_encoding("cl100k_base")  # closest match to GPT-3.5/Mistral-style encoding
    tokens = enc.encode(text)
    truncated = tokens[:n]
    return enc.decode(truncated)

def llm_says_toc_is_present(text: str, model: str = "mistral") -> bool:
    prompt = f"""
        You are a book-processing assistant.

        Your task is to determine whether the following text contains a Table of Contents (TOC).

        📌 Respond ONLY with one of the following exact options:
        - TOC_PRESENT
        - NO_TOC

        Do not generate any other text.
        Do not continue the story.

        TEXT START:
        \"\"\"{text}\"\"\"
        TEXT END
        """
        
    response = chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response["message"]["content"].strip().upper()

    print(f"[LLM TOC DETECTION] LLM response: {answer}")

    if "TOC_PRESENT" in answer:
        print("[LLM TOC DETECTION] LLM detected a TOC.")
        return True
    print("[LLM TOC DETECTION] LLM says no TOC.")
    return False

def remove_text_before_first_chapter(text: str) -> str:
    match = re.search(r'(chapter\s+\d+|chapter\s+[ivxlc]+)', text, re.IGNORECASE)
    if match:
        print(f"[REMOVE TEXT BEFORE 1ST CHAP] Cutting before: {match.group(0)} at position {match.start()}")
        return text[match.start():]
    print("[REMOVE TEXT BEFORE 1ST CHAP] No chapter heading found to cut from.")
    return text

def remove_toc(text: str) -> str:
    text = get_first_n_tokens(text, 1000)
    print(text)
    if llm_says_toc_is_present(text):
        return remove_text_before_first_chapter(text)
    return text

if __name__ == "__main__":
    start = time.time()
    file_path = "backend/test/data/echoes.txt"
    with open(file_path, 'r') as f:
        text = f.read()

    cleaned = remove_toc(text)
    print("\n[INFO] --- Cleaned text preview ---\n")
    print(f"{cleaned[:1000]} and the end is \n\n {cleaned[len(cleaned)-1000:]}\n")

    print(f"[INFO] Time elapsed {-start+time.time():.2f} seconds")