import os
import json

from pathlib import Path
from ollama import chat

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
        print(f"[INFO] Summarizing chunk {id}...")
        summary = summarize_chunk_with_mistral(chunk, id)
        chapter_breakdown.append(summary)

    return chapter_breakdown

def build_synopsis(chapter_breakdown) -> str: # First 5 chapters though
    context = "\n".join([c["summary"] for c in chapter_breakdown[:5]])
     
    prompt = (
        f"You are a professional editor writing a short synopsis for a book.\n\n"
        # f"Book title: '{book_title}'\n\n"
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
