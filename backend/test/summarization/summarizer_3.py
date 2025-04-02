import time
from ollama import chat
import re 
from typing import List
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
import os
import json
import time

with open("backend/test/data/alice_in_wonderland.txt", "r") as file:
    dummy_text = file.read()

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

def summarize_chunk_with_mistral(chunk_text: str, chunk_id: int) -> dict:
    
    prompt = (
        f"Summarize the following book passage into a concise 100 word text.\n"
        f"- Skip any generic introduction or explanations about the book, chapter or the author.\n"
        f"- Focus on what happens, key characters, or any important developments.\n"
        f"- Write in a direct tone that sounds like a compelling recap, not like a school report.\n\n"
        f"{chunk_text}\n\n"
        f" Use vivid but concise language, think like a movie recap."
    )
    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "chunk_id": chunk_id,
        "raw_output": response["message"]["content"]
    }

def summarize_all_chunks(chunks) -> dict:

    summarized_chunks = []

    for id, chunk in enumerate(chunks):
        print(f"[INFO] Summarizing chunk {id}...")
        summary = summarize_chunk_with_mistral(chunk, id)
        summarized_chunks.append(summary)

    return {
        "summary": summarized_chunks
    }


if __name__ == "__main__":
    start_total = time.time()

    print(f"📚 Splitting book into chapters...")
    chunks = split_into_chapters(dummy_text)

    print(f"✅ {len(chunks)} chunks created. Starting summarization...\n")

    start_summarization = time.time()
    result = summarize_all_chunks(chunks)
    end_summarization = time.time()

    print(f"\n⚡ Summarization completed in {end_summarization - start_summarization:.2f} seconds.")

    for chapter, summary in enumerate(result["summary"]):
        print(f"=== CHAPTER {chapter} ===")
        print(summary)

    filename = f"backend/test/summarization/summaries/alice_vivid_prompt_2.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(result, f, indent=4)
    print(f"✅ Summaries saved to {filename}.\n")

