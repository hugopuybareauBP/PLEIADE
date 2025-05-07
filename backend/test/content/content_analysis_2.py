# backend/test/content/content_analysis_2.py

import json
import time
import re
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

def build_time_period(synopsis, summaries):
    print(f"[BUILD_TIME_PERIOD] Building time period...")
    context = "\n".join(summaries[:5])

    prompt = (
        f"Based on the synopsis and chapters below, identify the time period covered by the book (e.g., 'Present day', '2030-2045', '19th century to now').\n"
        f"Consider historical events, cultural references, and any other relevant details.\n"
        f"The output should be maximum 10 words.\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"Chapter summaries:\n{context}"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a book publishing assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content

def build_genres(synopsis, summaries):
    print(f"[BUILD_GENRES] Building genres...")
    context = "\n".join(summaries[:5])

    prompt = (
        f"Based on the synopsis and chapters below, identify the genres of the book (e.g., 'Science Fiction', 'Romance', 'Historical Fiction').\n"
        f"Consider themes, characters, and any other relevant details.\n"
        f"**Just give 3 genres, separated by commas. Do not make a sentence or add any words.**\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"Chapter summaries:\n{context}"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a book publishing assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content

def build_tone(synopsis, summaries):
    print(f"[BUILD_TONE] Building tone...")
    context = "\n".join(summaries[:5])

    prompt = (
        f"Based on the synopsis and chapters below, identify the tone of the book (e.g., 'Serious', 'Humorous', 'Dark').\n"
        f"Consider writing style, character interactions, and any other relevant details.\n"
        f"**Just give 3 tones, separated by commas. Do not make a sentence or add any other words/number.**\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"Chapter summaries:\n{context}"
    )
    
    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a book publishing assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content

def build_keywords(synopsis, summaries):
    print(f"[BUILD_KEYWORDS] Building keywords...")
    context = "\n".join(summaries[:5])

    prompt = (
        f"Based on the synopsis and chapters below, identify 8 keywords that best represent the book.\n"
        f"Consider themes, characters, and any other relevant details.\n"
        f"**Just give 8 keywords, separated by commas. Do not make a sentence or add any other words/number.**\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"Chapter summaries:\n{context}"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a book publishing assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content

# def parse_keywords(raw_output: str):
#     # remove numbered list and commas
#     cleaned = re.sub(r"\d+\.\s*", "", raw_output.strip())
#     return [kw.strip().strip(",") for kw in cleaned.split(",") if kw.strip()]

# def parse_numbered_line(raw_output: str) -> str:
#     match = re.search(r"\d+\.\s*(.*)", raw_output.strip())
#     if match:
#         return match.group(1).strip()
#     return raw_output.strip()

if __name__ == '__main__':
    start = time.time()
    with open("backend/test/content/dumps/synopsis_echoes_2.json", "r") as f:
        data = json.load(f)
    synopsis = data["synopsis"]

    with open("backend/test/summarization/summaries/echoes_azure_1.json", "r") as f:
            data = json.load(f)
            summaries = [summary["raw_output"] for summary in data["summary"]]

    time_period = build_time_period(synopsis, summaries)
    print(f"[BUILD_TIME_PERIOD] Time period: {time_period}")
    print(f"[BUILD_TIME_PERIOD] Tile elapsed : {time.time()-start:.2f} seconds !")

    # genres = build_genres(synopsis, summaries)
    # print(f"[BUILD_GENRES] Genres: {genres}")
    # print(f"[BUILD_GENRES] Tile elapsed : {time.time()-start:.2f} seconds !")

    # tone = build_tone(synopsis, summaries)
    # print(f"[BUILD_TONE] Tone: {tone}")
    # print(f"[BUILD_TONE] Tile elapsed : {time.time()-start:.2f} seconds !")

    # keywords = build_keywords(synopsis, summaries)
    # print(f"[BUILD_KEYWORDS] Keywords: {keywords}")
    # print(f"[BUILD_KEYWORDS] Tile elapsed : {time.time()-start:.2f} seconds !")

