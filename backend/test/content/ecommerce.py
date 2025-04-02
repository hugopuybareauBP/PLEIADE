import json
import os
import time

from ollama import chat
from rich.console import Console
from rich.panel import Panel

# Initialize console
console = Console()

with open("backend/test/content/dumps/synopsis_alice.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    book_title = data["book_title"]
    synopsis = data["synopsis"]

def generate_ecommerce_description(book_title: str, synopsis: str) -> str:
    prompt = (
        f"You are a professional copywriter creating an e-commerce book description.\n\n"
        # f"Book title: '{book_title}'\n\n"
        f"Here is a short synopsis of the book:\n"
        f"{synopsis}\n\n"
        f"Based on this, write a compelling, professional product description including:\n"
        f"- A strong, attention-grabbing hook\n"
        f"- A short synopsis based on the summary\n"
        f"- A few bullet points about what readers will discover or enjoy\n"
        f"- A closing sentence that encourages the reader to get the book\n\n"
        f"Make it exciting and accessible, like something on Amazon. Do not mention that this is based on a summary or say that it’s written by an AI."
    ) 

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

if __name__ == "__main__":
    start = time.time()
    console.print(Panel(f"[bold cyan] Generating e-commerce description for : [green]{book_title}[/]"))
    description = generate_ecommerce_description(book_title, synopsis)
    console.print(Panel(f"[bold magenta]E-commerce Description:\n{description}[/]"))
    console.print(Panel(f"[bold green]Tile elapsed : {time.time()-start:.2f} seconds ![/]"))

