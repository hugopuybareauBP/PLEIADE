# backend/app/generation/llm.py

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
    print(f"[INFO] Building synopsis...")
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

def build_ecommerce_desc(synopsis) -> str:
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