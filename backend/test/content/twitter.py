import json
import time
from ollama import chat
from rich.console import Console

console = Console()

with open("backend/test/content/dumps/synopsis_echoes_2.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    # book_title = data["book_title"]
    synopsis = data["synopsis"]

def generate_tweets(synopsis: str) -> str:
    prompt = (
        f"You are a social media content writer for a publishing house.\n\n"
        f"Based on the following synopsis, generate a creative tweet that promote the book with the following synopsis.\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"The tweet should be punchy, engaging, and fit within 280 characters. "
        f"Use a witty, modern tone. Finish with 3 different hashtags and don't mention AI or that it is based on a summary.\n"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": 0.2
        }
    )

    return response["message"]["content"]

if __name__ == "__main__":
    start = time.time()
    console.print(f"[bold cyan]Generating tweet[/]")
    tweets = generate_tweets(synopsis)
    console.print(f"[bold magenta]Generated Tweets:\n{tweets}[/]")
    console.print(f"[bold green]Time elapsed: {time.time() - start:.2f} seconds[/]")
