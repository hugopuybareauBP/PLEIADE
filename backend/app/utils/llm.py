# backend/app/generation/llm.py

import json
import re

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
        print(f"[BUILD_CHAPTER_BREAKDOWN] Summarizing chunk {id}...")
        summary = summarize_chunk_with_mistral(chunk, id)
        chapter_breakdown.append(summary)

    return chapter_breakdown

def build_impact_analysis(chapter_breakdown) -> str:
    print(f"[BUILD_IMPACT_ANALYSIS] Building impact analysis...")
    context = "\n".join([c["raw_output"] for c in chapter_breakdown])

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

def parse_impact_analysis_output(raw_text: str) -> dict:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        print("[ANALYSIS_PARSER] Raw text is not JSON, falling back to text parsing.")

        strengths_match = re.search(r"\*\*Strengths:\*\*(.*?)(\*\*Weaknesses:\*\*|$)", raw_text, re.DOTALL)
        weaknesses_match = re.search(r"\*\*Weaknesses:\*\*(.*)", raw_text, re.DOTALL)

        strengths_raw = strengths_match.group(1).strip() if strengths_match else ""
        weaknesses_raw = weaknesses_match.group(1).strip() if weaknesses_match else ""

        strengths = [re.sub(r"^\d+\.\s*", "", line.strip()) for line in strengths_raw.split("\n") if line.strip()]
        weaknesses = [re.sub(r"^\d+\.\s*", "", line.strip()) for line in weaknesses_raw.split("\n") if line.strip()]

        return {
            "strengths": strengths,
            "weaknesses": weaknesses
        }
                

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

def build_ecommerce_description(synopsis: str) -> str:
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

def parse_ecommerce_output(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print("[ECOMMERCE_PARSER] Raw text is not JSON, falling back to text parsing.")
        lines = raw.splitlines()
        description = []
        bullets = []
        closing = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if re.match(r"^[-•]", line): # we look for a bullet point
                bullets.append(re.sub(r"^[-•]\s*", "", line))
            else:
                description.append(line)

        # # Separate closing from description (last 1-2 lines)
        # if len(description) >= 2:
        #     closing = description[-1]
        #     description = description[:-1]

        return {
            "description": description,
            "bullets": bullets,
            "closing": []
        }

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

def build_impact_analysis(chapter_breakdown) -> str:
    print(f"[BUILD_IMPACT_ANALYSIS] Building impact analysis...")
    context = "\n".join([c["summary"] for c in chapter_breakdown[:5]])
    
    prompt = (
        f"You are a professional book analyst. Based on the chapter summaries below, write a list of strengths and weaknesses "
        f"for this book. Focus on writing style, structure, clarity, examples, and depth of content.\n\n"
        f"Do not reference chapters directly. Instead, extract high-level impressions.\n\n"
        f"Chapter summaries:\n{context}\n\n"
        f"Return two separate lists:\n"
        f"- Strengths (5 items max)\n"
        f"- Weaknesses (5 items max)\n\n"
        f"Use bullet points and clear, concise language."
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]