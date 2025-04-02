import spacy
import time 
import re
from typing import List

from collections import Counter, defaultdict
from ollama import chat

with open("backend/test/data/romeo_and_juliet.txt", "r") as file:
    dummy_text = file.read()

dummy_text = dummy_text.lower()

start_time = time.time()

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

# NER
nlp = spacy.load("en_core_web_trf")
character_mentions = []

for chunk in chunks:
    doc = nlp(chunk)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            character_mentions.append(ent.text)

# Most common 
top_n = 5
top_characters = [name for name, _ in Counter(character_mentions).most_common(top_n)]
print(f"\nTop {top_n} characters: {top_characters}")

end_time = time.time()

print(f"[INFO] Elapsed time : {end_time - start_time:.2f} seconds")

# # Select chunks per character
# character_chunks = defaultdict(list)

# for char in top_characters:
#     for chunk in chunks:
#         if char in chunk:
#             character_chunks[char].append(chunk)

# # Profil generation
# def summarize_character_profile(character_name, chunk_list):
#     prompt = (
#         f"Write a detailed character profile of '{character_name}' based on the following book passages :\n\n"
#         + "\n\n".join(chunk_list)
#     )

#     response = chat(
#         model="mistral",
#         messages=[{"role": "user", "content": prompt}]
#     )

#     return response ["message"]["content"]

# # Test 
# for character in top_characters:
#     print(f"\n---------- Character profile : {character} ----------")
#     profile = summarize_character_profile(character, character_chunks[character])
#     print(profile)

