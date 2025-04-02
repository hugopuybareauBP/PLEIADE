import time 
import re 

from ollama import chat
from typing import List
from collections import Counter

with open("backend/test/data/test_summarization_2.txt", "r") as file:
    dummy_text = file.read()

dummy_text = dummy_text.lower()

# Chunking
def split_into_chapters(text: str, fallback_chunk_size: int = 1000) -> List[str]:

    # Content table detection 
    ct_pattern = re.compile(r"(table of contents|contents|toc)([\s\S]{0,10000})", re.IGNORECASE) # if i dont put the a limit, it will grab full book
    ct_match = re.search(ct_pattern, text)
        
    if ct_match: # found one
        print(f"CT detected")
        ct_block = ct_match.group(2)
        chapter_lines = re.findall(r'(chapter\s+(?:\d+|[ivxlc]+).*?)\n', ct_block, re.IGNORECASE)

        if chapter_lines:
            last_heading = chapter_lines[-1]
            heading_pattern = re.escape(last_heading.strip())
            last_heading_match = list(re.finditer(heading_pattern, text, re.IGNORECASE))

            if last_heading_match:
                ct_end = last_heading_match[0].end()
               #  print(f"Removed {text[:ct_end]}")
                text = text[ct_end:]
                    
    # Look for chapter in the text
    chapter_pattern = r'(chapter\s+(?:\d+|[ivxlc]+))\b' # strict so it doesnt match 'in this chapter ...' 
    chapter_matches = list(re.finditer(chapter_pattern, text, re.IGNORECASE))

    if len(chapter_matches) >= 2:
        print(f"{len(chapter_matches)} chapters detected via headings.")
        chunks = []
        for i in range(len(chapter_matches)):
            start = chapter_matches[i].start()
            end = chapter_matches[i + 1].start() if i + 1 < len(chapter_matches) else len(text)
            chunks.append(text[start:end].strip())
        return chunks

    # split into fixed-length chunks
    print("No structure found — fallback to chunking.")
    words = text.split()
    chunks = []
    for i in range(0, len(words), fallback_chunk_size):
        chunk = ' '.join(words[i:i+fallback_chunk_size])
        chunks.append(chunk)
    return chunks

# chunks = split_into_chapters(dummy_text, 1000)
chunks = [dummy_text]

def extract_character_llm(chunk: str) -> List[str]:
    prompt = (
        "List all named characters that appear in the following text. \n\n"
        f"{chunk}\n\n"
        "Return only the names, separated by commas."
    )

    response = chat(
        model='mistral',
        messages=[{"role": "user", "content": prompt}]
    )

    raw_text = response["message"]["content"]
    characters = re.split(r',\s*', raw_text.strip())
    return [c.strip() for c in characters if c]

def get_top_characters(text: str, top_k: int=10) -> List[str]:
    all_names = []
    chunks = split_into_chapters(text, 1000)
    
    for i, chunk in enumerate(chunks):
        print(f"[INFO] Extracting characters from chunk {i+1}/{len(chunks)}...")
        try:
            characters = extract_character_llm(chunk)
            all_names.extend(characters)
        except Exception as e:
            print(f"[ERROR] Error processing chunk {i}: {e}")
            continue

    counts = Counter(all_names)
    return counts.most_common(top_k)

def summarize_character_life(text: str, character: str) -> str:
    prompt = (
        f"Based only on the following passages, write exactly ONE short sentence that summarizes who '{character}' is. "
        f"Do not write more than one sentence.\n\n"
        f"{text}"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

if __name__ == '__main__':
    start_1 = time.time()
    print("[INFO] Extracting Top Characters...")
    top_characters = get_top_characters(dummy_text, 5)
    print("\nTop Characters:", top_characters)
    print(f"[INFO] Elapsed time for top characters recognition: {time.time() - start_1:.2f} seconds")
    start_2 = time.time()
    print("\n[INFO] Summarizing characters...\n")
    for name, count in top_characters:
        print(f"🔹 {name} (mentioned {count} times):")
        summary = summarize_character_life(chunks, name)
        print(summary)
        print("-" * 80)
    print(f"\n[INFO] Elapsed time for creating profiles: {time.time() - start_2:.2f} seconds")
    print(f"[INFO] Total elapsed time : {time.time() - start_1:.2f} seconds")