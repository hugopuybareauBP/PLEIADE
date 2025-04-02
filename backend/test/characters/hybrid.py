from ollama import chat
from collections import Counter
from typing import List

import re
import time
import spacy

with open("backend/test/data/moby_dick.txt", "r") as file:
    dummy_text = file.read()

nlp = spacy.load("en_core_web_trf")

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

chunks = split_into_chapters(dummy_text, 1000)
# chunks = [dummy_text]

# Score chunks by character count
def count_characters_mentions(chunks, character_name):
    character_name = character_name.lower()
    scored = []
    for chunk in chunks:
        doc = nlp(chunk)
        mentions = sum(1 for ent in doc.ents if ent.label_ == "PERSON" and ent.text.lower() == character_name)
        scored.append((chunk, mentions))
    return scored

def get_top_chunks_for_character(chunks, character_name, top_k=3):
    scored = count_characters_mentions(chunks, character_name)
    sorted_chunks = sorted(scored, key=lambda x: x[1], reverse=True)
    top_chunks = [chunk for chunk, score in sorted_chunks[:top_k] if score > 0]
    return top_chunks

def generate_character_profile(character_name, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    prompt = (
        f"Based only on the following passages, write exactly ONE short sentence that summarizes who '{character_name}' is. "
        f"Do not write more than one sentence.\n\n"
        f"{context}\n\n"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

if __name__ == '__main__':
    characters = ["Ahab", "Ishmael", "Queequeg"]
    start = time.time()
    for character in characters:
        print(f"[INFO] Extracting chunks for {character}...")
        top_chunks = get_top_chunks_for_character(chunks, character)
        print(f"[INFO] Top chunks for {character}:")
    #     if top_chunks:
    #         print(f"[INFO] Generating profile for {character}...")
    #         profile = generate_character_profile(character, top_chunks)
    #         print(f"[INFO] Profile for {character}:\n{profile}")
    #     else:
    #         print(f"[INFO] No relevant chunks found for {character}.")
    # print(f"[INFO] Total time taken: {time.time() - start:.2f} seconds.")



