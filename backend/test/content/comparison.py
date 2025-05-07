# backend/test/content/comparison.py

import json
import re
import time
import os

from openai import AzureOpenAI

# Azure OpenAI Configuration
api_version = "2024-12-01-preview"
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_INFERENCE_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_INFERENCE_ENDPOINT")
AZURE_OPENAI_MODEL_NAME = os.getenv("AZURE_OPENAI_INFERENCE_MODEL_NAME")

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=api_version,
)

def build_comparison(synopsis, keywords):
    prompt = (
        f"You are a publishing expert.\n"
        f"Based on the synopsis and the keywords below, suggest 5 books that are similar in content, themes and audience.\n"
        f"Return the response in JSON format with the following structure:\n"
        f"[{{\"author\": \"Author Name\", \"title\": \"Book Title\", \"note\": \"Short note about the book\"}}, ...]\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"Keywords:\n{keywords}\n\n"
    )
    
    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a publishing expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content

def parse_model_json_response(raw_output: str) -> dict | None:
    # Remove markdown code block wrappers like ```json
    cleaned = re.sub(r"^```(?:json|python)?|```$", "", raw_output.strip(), flags=re.IGNORECASE | re.MULTILINE).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        return None


if __name__ == "__main__":
    start = time.time()
    with open("backend/test/content/dumps/synopsis_echoes.json", "r") as f:
        data = json.load(f)
    synopsis = data["synopsis"]

    keywords = [
        "curiosity",
        "imagination",
        "absurdity",
        "transformation",
        "identity",
        "surrealism",
        "exploration",
        "whimsy"
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
    print(f"\n\n [PARSED COMPARISON] {parse_model_json_response(comparison)}")
    print(f"Execution time: {time.time() - start:.2f} seconds")