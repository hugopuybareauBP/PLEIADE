import json
import time
import os 

from ollama import chat
from rich.console import Console
from rich.panel import Panel

# Initialize console
console = Console()

book_title = "Alice in Wonderland"

def generate_synopsis_from_summaries(book_title: str, summaries: str) -> str:
    summary = "\n".join(summaries[:5])
     
    prompt = (
        f"You are a professional editor writing a short synopsis for a book.\n\n"
        # f"Book title: '{book_title}'\n\n"
        f"Below are key points and chapter-level summaries extracted from the book:\n\n"
        f"{summary}\n\n"
        f"Using this information, write a polished 2–3 sentence synopsis in the style of a book jacket blurb.\n"
        f"The synopsis should:\n"
        f"- Capture the essence and themes of the book\n"
        f"- Sound professional and high-level (not like a chapter summary)\n"
        f"- Avoid bullet points and lists\n"
        f"- Be suitable for an e-commerce product page or publisher's back cover\n"
        f"- Do not mention summaries or chapters\n"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

if __name__ == "__main__":
    start = time.time()
    filepath = "backend/test/summarization/summaries/alice_vivid_prompt_2.json"
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    summaries = [summary["raw_output"] for summary in data["summary"]]

    console.print(Panel(f"[bold cyan] Generating synopsis : [green]{book_title}[/]"))
    synospis = generate_synopsis_from_summaries(book_title, summaries)
    synopsis_dict = {
        "book_title": book_title,
        "synopsis": synospis
    }
    console.print(Panel(f"[bold magenta]Synopsis:\n{synospis}[/]"))
    console.print(Panel(f"[bold green]Tile elapsed : {time.time()-start:.2f} seconds ![/]"))

    dumpname = f"backend/test/content/dumps/synopsis_alice.json"
    os.makedirs(os.path.dirname(dumpname), exist_ok=True)
    with open(dumpname, "w") as f:
        json.dump(synopsis_dict, f, indent=4)



