import json
import os
import time

from ollama import chat
from rich.console import Console
from rich.panel import Panel

# Initialize console
console = Console()

with open("backend/test/content/dumps/synopsis_echoes_2.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    synopsis = data["synopsis"]

def generate_ecommerce_description(synopsis: str) -> str:
    prompt = (
        f"You are a professional copywriter creating an e-commerce book description.\n\n"
        f"Here is a short synopsis of the book:\n"
        f"{synopsis}\n\n"
        f"Based on this, return a compelling and professional product description as a JSON object with this format:\n"
        f"{{\n"
        f"  \"description\": [\"A strong, attention-grabbing hook\", \"Followed by a few short, exciting sentences summarizing the book\"],\n"
        f"  \"bullets\": [\"Key takeaway 1\", \"Key takeaway 2\", \"Key takeaway 3\"],\n"
        f"  \"closing\": \"A persuasive sentence encouraging the user to buy the book.\"\n"
        f"}}\n\n"
        f"Make it exciting and accessible like something found on Amazon. Do NOT include markdown or explanations outside the JSON."
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

if __name__ == "__main__":
    start = time.time()
    console.print(f"[bold cyan] Generating e-commerce description[/]")
    for i in range(5):
        description = generate_ecommerce_description(synopsis)
        console.print(f"[bold magenta]E-commerce Description:\n{description}[/]")
        console.print(f"[bold green]Time elapsed : {time.time()-start:.2f} seconds ![/]")

