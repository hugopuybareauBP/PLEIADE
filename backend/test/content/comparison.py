# backend/test/content/comparison.py

import json
import re
import time

from ollama import chat

def build_comparison(synopsis, keywords):
    prompt = (
        f"You are a publishing expert.\n"
        f"Based on the synopsis and the keywords below, suggest 5 books that are similar in content, themes and audience.\n"
        f"Return the response in JSON format with the following structure:\n"
        f"[{{\"author\": \"Author Name\", \"title\": \"Book Title\", \"note\": \"Short note about the book\"}}, ...]\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"Keywords:\n{keywords}\n\n"
    )
    
    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

def parse_comparison(raw_output):
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        results = []

        # Split on entry numbers (1., 2., etc.)
        entries = re.split(r"\n?\s*\d+\.\s*", raw_output.strip())

        for entry in entries:
            if not entry.strip():
                continue

            author, title, note = "", "", ""

            # === CASE 1: Oneliner format ===
            if "Short Note:" in entry:
                author_match = re.search(r"Author:\s*(.*?),\s*Title:", entry)
                title_match = re.search(r"Title:\s*\"?(.*?)\"?,\s*Short Note:", entry)
                note_match = re.search(r"Short Note:\s*(.*)", entry, re.DOTALL)
                
                if author_match and title_match and note_match:
                    author = author_match.group(1).strip()
                    title = title_match.group(1).strip().strip('"')
                    note = note_match.group(1).strip()

            # === CASE 2: Multiline format ===
            else:
                lines = entry.strip().splitlines()
                for line in lines:
                    if line.strip().lower().startswith("author:"):
                        author = line.split(":", 1)[1].strip()
                    elif line.strip().lower().startswith("title:"):
                        title = line.split(":", 1)[1].strip().strip('"')
                    elif line.strip().lower().startswith("note:"):
                        note = line.split(":", 1)[1].strip()
                    else:
                        # continuation of the note
                        note += " " + line.strip()

            if author and title:
                results.append({
                    "author": author,
                    "title": title,
                    "note": note.strip()
                })

        return json.dumps(results, indent=4)


if __name__ == "__main__":
    start = time.time()
    with open("backend/test/content/dumps/synopsis_echoes.json", "r") as f:
        data = json.load(f)
    synopsis = data["synopsis"]

    keywords = [
        'Project Echo',
        'Dr. Evelyn Porter',
        'Digital purgatory',
        'Consciousness digitization',
        'Memory',
        'Identity',
        'Enigmatic adversary',
        'Sentinels'
    ]

    # keywords = [
    #     'Alice',
    #     'Wonderland',
    #     'Rabbit',
    #     'Cheshire Cat',
    #     'Tears',
    #     'Caucus-Race',
    #     'Caterpillar',
    #     'Red Queen',
    #     'Underland'
    # ]

    comparison = build_comparison(synopsis, keywords)
    print(f"[COMPARISON] Response: {comparison}")
    print(f"\n\n [PARSED COMPARISON] {parse_comparison(comparison)}")
    print(f"Execution time: {time.time() - start:.2f} seconds")