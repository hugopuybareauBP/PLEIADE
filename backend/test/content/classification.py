# backend/test/content/classification.py

import time 
import json
import re

from ollama import chat

def build_primary_thema_code(synopsis, summaries):
    context = "\n".join(summaries[:3])
    prompt = (
        # f"You are a publishing metadata assistant.\n"
        f"Based on the synopsis below,"
        f"Identify the **most appropriate thema subject classification code** for this book.\n"
        f"Only return the 2-letter Thema code (e.g. 'UB', 'KJ', 'PDR')\n"
        # f"{synopsis}\n\n"
        f"Chapter summaries:\n"
        f"{context}"
    )

    # print(prompt)

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

if __name__ == "__main__":
    start = time.time()
    with open("backend/test/content/dumps/synopsis_alice.json", "r") as f:
        data = json.load(f)
    synopsis = data["synopsis"]

    with open("backend/test/summarization/summaries/alice_vivid_prompt_2.json", "r") as f:
            data = json.load(f)
            summaries = [summary["raw_output"] for summary in data["summary"]]
    
    primary_thema_code = build_primary_thema_code(synopsis, summaries)
    print(f"{primary_thema_code}")
    print(f"Execution time: {time.time() - start:.2f} seconds")

