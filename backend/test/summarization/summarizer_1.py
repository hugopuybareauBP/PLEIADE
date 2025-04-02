import time
from ollama import chat
import re 
from typing import List

from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
from rich.pretty import Pretty

with open("backend/test/data/alice_in_wonderland.txt", "r") as file:
    dummy_text = file.read()

# print(dummy_text[:1000])

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
        f"Summarize the following book passage in 3 bullet points. "
        f"Focus on important events and characters.\n\n{chunk_text}"
    )

    start = time.time()

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    end = time.time()
    elapsed = end - start

    print(f"[INFO] --- Chunk {chunk_id} summarized in {elapsed:.2f} seconds. ---")
    return {
        "chunk_id": chunk_id,
        "summary": response["message"]["content"]
    }

console = Console()

def summarize_all_chunks(chunks) -> dict:

    summarized_chunks = []
    with Progress() as progress:
        task = progress.add_task("[cyan]Summarizing...", total=len(chunks))

        for id, chunk in enumerate(chunks):
            console.log(f"[bold yellow] Summarizing chunk {id}...[/]")
            summary = summarize_chunk_with_mistral(chunk, id)
            summarized_chunks.append(summary)
            progress.update(task, advance=1)

    return {
        "summary": summarized_chunks
    }

# test
if __name__ == "__main__":
    console.print(Panel("[bold blue]📚 Splitting book into chapters..."))
    chunks = split_into_chapters(dummy_text)
    console.print(f"[green]✅ {len(chunks)} chapters detected.\n")
    result = summarize_all_chunks(chunks)
    console.print(Panel("[bold green]🎉 All chunks summarized. Summary result below:\n"))
    console.print(Pretty(result["summary"], expand_all=True))
