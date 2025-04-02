import time
from ollama import chat
import re 
from typing import List
from collections import defaultdict
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
import time

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
        f"You are analyzing a novel. For the following passage:\n"
        f"1. List the characters that appear or are mentioned.\n"
        f"2. For each character, summarize their actions or role in this passage.\n"
        f"3. If there are important events, briefly list them.\n\n"
        f"---\n\n{chunk_text}\n\n---\n"
        f"Format your output as:\n"
        f"- Characters: [list]\n"
        f"- Character Notes:\n  - Name: details...\n  - Name: details...\n"
        f"- Events: [list]"
)

    start = time.time()

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    end = time.time()
    elapsed = end - start

    # print(f"[INFO] --- Chunk {chunk_id} summarized in {elapsed:.2f} seconds. ---")
    return {
        "chunk_id": chunk_id,
        "raw_output": response["message"]["content"]
    }

def summarize_all_chunks(chunks) -> dict:

    summarized_chunks = []

    with Progress() as progress:
        task = progress.add_task("[cyan]Summarizing...", total=len(chunks))
        for id, chunk in enumerate(chunks):
        # print(f"[INFO] Summarizing chunk {id}...")
            summary = summarize_chunk_with_mistral(chunk, id)
            summarized_chunks.append(summary)
            progress.update(task, advance=1)

    return {
        "summary": summarized_chunks
    }

def extract_character_notes(raw_summary: str):
    character_notes = {}
    current_char = None

    for line in raw_summary.splitlines():
        line = line.strip()
        if line.startswith("- Characters:"):
            characters_line = line.split(":", 1)[1]
            characters = [c.strip() for c in characters_line.split(",") if c]
        elif line.startswith("- Character Notes:"):
            continue
        elif line.startswith("- Events:"):
            break
        elif line.startswith("- ") or line.startswith("• "):
            match = re.match(r"[-•]\s*(\w+):\s*(.*)", line)
            if match:
                char_name, note = match.groups()
                character_notes[char_name] = note
    return character_notes

def aggregate_character_notes(summaries, top_c: int):
    aggregated_notes = defaultdict(list)
    mention_counts = defaultdict(int)

    for summary in summaries:
        character_notes = extract_character_notes(summary["raw_output"])
        for char, note in character_notes.items():
            aggregated_notes[char].append(note)
            mention_counts[char] += 1    
    
    top_characters = sorted(mention_counts.items(), key=lambda x: x[1], reverse=True)[:top_c]
    console.print("\n[bold blue]🏆 Top 5 characters (by mentions):[/]")
    for char, count in top_characters:
        console.print(f"• {char} ({count} mentions)")
    top_character_names = {char for char, _ in top_characters}

    filtered_notes = {char: aggregated_notes[char] for char in top_character_names}
    return filtered_notes

def generate_final_profiles(character_memory):
    profiles = {}

    for character, notes in character_memory.items():
        prompt = (
            f"Based on the following notes about the character {character}"
            f"write a complete character profile including:\n"
            f"- Personality traits\n- Role in the story\n- Key events and relationships\n\n"
            f"Notes:\n{chr(10).join(['- ' + n for n in notes])}"
        )

        response = chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )

        profiles[character] = response["message"]["content"]

    return profiles

if __name__ == "__main__":
    console = Console()
    start_total = time.time()

    console.print(Panel("[bold cyan]📚 Splitting book into chapters..."))
    chunks = split_into_chapters(dummy_text)

    console.print(f"[bold green]✅ {len(chunks)} chunks created. Starting summarization...\n")

    start_summarization = time.time()
    result = summarize_all_chunks(chunks)
    end_summarization = time.time()

    console.print(f"\n[bold yellow]⚡ Summarization completed in {end_summarization - start_summarization:.2f} seconds.")

    console.print("\n[bold cyan]🔍 Aggregating character notes...")
    start_aggregation = time.time()
    character_memory = aggregate_character_notes(result["summary"], top_c=5)
    end_aggregation = time.time()

    console.print(f"[green]✅ Aggregation completed in {end_aggregation - start_aggregation:.2f} seconds.")

    console.print("\n[bold magenta]🧠 Generating final character profiles...")
    start_profiles = time.time()
    final_profiles = generate_final_profiles(character_memory)
    end_profiles = time.time()

    console.print(f"[green]✅ Profile generation completed in {end_profiles - start_profiles:.2f} seconds.")

    total_time = time.time() - start_total
    console.print(Panel(f"[bold green]🎉 Done! Total runtime: {total_time:.2f} seconds."))

    for character, profile in final_profiles.items():
        console.print(Panel(f"[bold blue]=== {character.upper()} ===", expand=False))
        console.print(profile)


