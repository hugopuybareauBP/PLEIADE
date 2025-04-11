# backend/app/generation/llm.py

import json
import re

from pathlib import Path
from ollama import chat

### ANALYSIS DETAILS ###

def summarize_chunk_with_mistral(chunk_text: str, chunk_id: int) -> dict:
    
    prompt = (
        f"Summarize the following book passage into a concise 100 word text.\n"
        f"- Skip any generic introduction or explanations about the book, chapter or the author.\n"
        f"- Focus on what happens, key characters, or any important developments.\n"
        f"- Write in a direct tone that sounds like a compelling recap, not like a school report.\n\n"
        f"{chunk_text}\n\n"
        f" Use vivid but concise language, think like a movie recap."
    )
    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "title": f"Chapter {chunk_id + 1}",
        "summary": response["message"]["content"]
    }

def build_chapter_breakdown(chunks) -> dict:

    chapter_breakdown = []

    for id, chunk in enumerate(chunks):
        print(f"[BUILD_CHAPTER_BREAKDOWN] Summarizing chunk {id}...")
        summary = summarize_chunk_with_mistral(chunk, id)
        chapter_breakdown.append(summary)

    return chapter_breakdown

def build_impact_analysis(chapter_breakdown) -> str:
    print(f"[BUILD_IMPACT_ANALYSIS] Building impact analysis...")
    context = "\n".join([c["summary"] for c in chapter_breakdown])

    prompt = (
        f"You are a professional book analyst.\n"
        f"Based on the chapter summaries below, write a list of 5 strengths and 5 weaknesses for this book.\n"
        f"Focus on writing style, structure, clarity, examples, and depth of content.\n\n"
        f"Respond with valid **minified JSON** ONLY. Do not include markdown, no explanations, no labels.\n"
        "Format:\n{\"strengths\": [\"...\"], \"weaknesses\": [\"...\"]}\n\n"
        f"Chapter summaries:\n{context}"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    print(f"[BUILD_IMPACT_ANALYSIS] Response: {response['message']['content']}")

    return response["message"]["content"]

### MARKETING DETAILS ###

def build_ecommerce_description(synopsis: str) -> str:
    prompt = (
        f"You are a professional copywriter writing an e-commerce book description.\n\n"
        f"Here is a short synopsis of the book you have to describe.\n"
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

def build_tweet(synopsis) -> str:
    prompt = (
        f"You are a social media content writer for a publishing house.\n\n"
        f"Based on the following synopsis, generate a creative tweets that promote the book with the following synopsis.\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"The tweet should be punchy, engaging, and fit within 280 characters. "
        f"Use a witty, modern tone. Finish with 3 different hashtags and don't mention AI or that it is based on a summary.\n"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

### OVERVIEW DETAILS ###

def build_synopsis(chapter_breakdown) -> str: # First 5 chapters though
    print(f"[BUILD_SYNOPSIS] Building synopsis...")
    context = "\n".join([c["summary"] for c in chapter_breakdown[:5]])
     
    prompt = (
        f"You are a professional editor writing a short synopsis for a book.\n\n"
        f"Below are key points and chapter-level summaries extracted from the book:\n\n"
        f"{context}\n\n"
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

def build_time_period(synopsis, chapter_breakdown):
    print(f"[BUILD_TIME_PERIOD] Building time period...")
    context = "\n".join([c["summary"] for c in chapter_breakdown[:5]])

    prompt = (
        f"Based on the synopsis and chapters below, identify the time period covered by the book (e.g., 'Present day', '2030-2045', '19th century to now').\n"
        f"Consider historical events, cultural references, and any other relevant details.\n"
        f"One sentence is enough.\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"Chapter summaries:\n{context}"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

def build_genres(synopsis, chapter_breakdown):
    print(f"[BUILD_GENRES] Building genres...")
    context = "\n".join([c["summary"] for c in chapter_breakdown[:5]])

    prompt = (
        f"Based on the synopsis and chapters below, identify the genres of the book (e.g., 'Science Fiction', 'Romance', 'Historical Fiction').\n"
        f"Consider themes, characters, and any other relevant details.\n"
        f"**Just give 3 genres, separated by commas. Do not make a sentence or add any words.**\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"Chapter summaries:\n{context}"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

def build_tone(synopsis, chapter_breakdown):
    print(f"[BUILD_TONE] Building tone...")
    context = "\n".join([c["summary"] for c in chapter_breakdown[:5]])

    prompt = (
        f"Based on the synopsis and chapters below, identify the tone of the book (e.g., 'Serious', 'Humorous', 'Dark').\n"
        f"Consider writing style, character interactions, and any other relevant details.\n"
        f"**Just give 3 tones, separated by commas. Do not make a sentence or add any other words/number.**\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"Chapter summaries:\n{context}"
    )
    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

def build_keywords(synopsis, chapter_breakdown):
    print(f"[BUILD_KEYWORDS] Building keywords...")
    context = "\n".join([c["summary"] for c in chapter_breakdown[:5]])

    prompt = (
        f"Based on the synopsis and chapters below, identify 8 keywords that best represent the book.\n"
        f"Consider themes, characters, and any other relevant details.\n"
        f"**Just give 8 keywords, separated by commas. Do not make a sentence or add any other words/number.**\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"Chapter summaries:\n{context}"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]