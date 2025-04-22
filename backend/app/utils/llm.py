# backend/app/generation/llm.py

import os

from typing import List
from openai import AzureOpenAI

# Azure OpenAI Configuration
api_version = "2024-12-01-preview"
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_MODEL_NAME = os.getenv("AZURE_OPENAI_MODEL_NAME")

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=api_version,
)

### ANALYSIS DETAILS ###

def summarize_chunk_with_mistral(chunk_text: str, chunk_id: int) -> dict:
    
    prompt = (
        f"Summarize the following book passage into a concise 100 word text.\n"
        f"- Skip any generic introduction or explanations about the book, chapter or the author.\n"
        f"- Focus on what happens, key characters, or any important developments.\n"
        f"- Summarize this chapter based only on the provided text."
        f"- Do not invent characters or settings. If the text is vague, keep the summary general."
        f" {chunk_text}\n\n"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful summarization assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return {
        "chapter_name": f"Chapter {chunk_id+1}",
        "raw_output": response.choices[0].message.content
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
        f"Based on the chapter summaries below, write a list of 5 strengths and 5 weaknesses for this book.\n"
        f"Focus on writing style, structure, clarity, examples, and depth of content.\n\n"
        f"Respond with valid **minified JSON** ONLY. Do not include markdown, no explanations, no labels.\n"
        "Format:\n{\"strengths\": [\"...\"], \"weaknesses\": [\"...\"]}\n\n"
        f"Chapter summaries:\n{context}"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional book analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content

# Character profile generation

def build_character_candidates_from_chunk(text: str) -> List[str]:
    prompt = (
        f"Extract the full names of fictional characters explicitly mentioned in this book excerpt.\n"
        f"Only include clearly named characters (no pronouns, vague roles, or invented names).\n"
        f"Return as a bullet list.\n\n"
        f"{text}"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional literary analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=2048
    )

    return response.choices[0].message.content

def build_top_characters(unique_candidates: List[str], n: int = 10) -> str:
    prompt = (
        f"Here is a list of character names from a book:\n\n"
        + "\n".join(f"- {name}" for name in unique_candidates) +
        f"\n\nClean this list by:\n"
        f"- Merging duplicate names (e.g., 'The Hatter' and 'Mad Hatter')\n"
        f"- Removing generic or non-informative entries\n"
        f"- Returning at most {n} of the most important characters as a bullet list only.\n"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional book analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=1024
    )

    return response.choices[0].message.content

def build_character_profile(character_name: str, context: str) -> str:
    prompt = (
        f"Write a concise character profile for {character_name} using only the information below.\n"
        f"Return it as a JSON object like this:\n"
        f'{{"character_name": "{character_name}", "description": "<context-based summary>"}}\n'
        f"---\n{context}\n---"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a literary analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1024
    )

    return response.choices[0].message.content

# Location note generation

def build_location_candidates_from_chunk(text: str) -> str:
    prompt = (
        f"Extract the names of fictional or real locations explicitly mentioned in this book excerpt.\n"
        f"Include cities, buildings, landmarks, regions, and notable places. Exclude vague terms like 'the house' or 'the village'.\n"
        f"Return them as a bullet list.\n\n"
        f"{text}"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional literary analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=2048
    )

    return response.choices[0].message.content

def build_top_locations(unique_locations: List[str], n: int = 10) -> str:
    prompt = (
        f"Here is a list of locations from a book:\n\n"
        + "\n".join(f"- {name}" for name in unique_locations) +
        f"\n\nClean this list by:\n"
        f"- Merging duplicate locations (e.g., 'Core chamber' and 'Core')\n"
        f"- Removing generic or non-informative entries\n"
        f"- Returning at most {n} of the most important locations as a bullet list only.\n"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional book analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=1024
    )

    return response.choices[0].message.content

def build_location_note(location_name: str, context: str) -> str:
    prompt = (
        f"Write a short note about the location '{location_name}' using only the information below.\n"
        f"Return it as a JSON object like this:\n"
        f'{{"location_name": "{location_name}", "description": "<context-based summary>"}}\n'
        f"---\n{context}\n---"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a literary analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1024
    )

    return response.choices[0].message.content

### MARKETING DETAILS ###

def build_ecommerce_description(synopsis: str, title) -> str:
    prompt = (
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

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional copywriter creating an e-commerce book description."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content

def build_tweet(synopsis) -> str:
    prompt = (
        f"Based on the following synopsis, generate a tweet that promote the book with the following synopsis.\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"The tweet should be punchy, engaging, and fit within 280 characters. "
        f"Use a witty, modern tone. Finish with 3 different hashtags and don't mention AI or that it is based on a summary.\n"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a social media content writer for a publishing house."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content

### OVERVIEW DETAILS ###

def build_synopsis(chapter_breakdown, title) -> str: # First 5 chapters though
    print(f"[BUILD_SYNOPSIS] Building synopsis...")
    context = "\n".join([c["raw_output"] for c in chapter_breakdown[:5]])
     
    prompt = (
        f"Book title: '{title}'\n\n"
        f"Below are key points and chapter-level summaries extracted from the book:\n\n"
        f"{context}\n\n"
        f"Using ONLY this information, write a polished 2–3 sentence synopsis in the style of a book jacket blurb.\n"
        f"The synopsis should:\n"
        f"- Capture the essence and themes of the book\n"
        f"- Sound professional and high-level (not like a chapter summary)\n"
        f"- Avoid bullet points and lists\n"
        f"- Be suitable for an e-commerce product page or publisher's back cover\n"
        f"- Do not mention summaries or chapters\n"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional editor writing a short synopsis for a book."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content

def build_time_period(synopsis, chapter_breakdown):
    print(f"[BUILD_TIME_PERIOD] Building time period...")
    context = "\n".join([c["raw_output"] for c in chapter_breakdown[:3]])

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

def build_genres(synopsis, chapter_breakdown):
    print(f"[BUILD_GENRES] Building genres...")
    context = "\n".join([c["raw_output"] for c in chapter_breakdown[:5]])

    prompt = (
        f"Based on the synopsis and chapters below, identify the genres of the book (e.g., 'Science Fiction', 'Romance', 'Historical Fiction').\n"
        f"Consider themes, characters, and any other relevant details.\n"
        f"**Just give 3 genres, separated by commas. e.g (\"Technology, Business, Future Studies\").\n"
        f"Do not make a sentence or add any words.**\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"Chapter summaries:\n{context}"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional book analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content

def build_tone(synopsis, chapter_breakdown):
    print(f"[BUILD_TONE] Building tone...")
    context = "\n".join([c["raw_output"] for c in chapter_breakdown[:3]])

    prompt = (
        f"Based on the synopsis and chapters below, identify the tone of the book (e.g., 'Serious', 'Humorous', 'Dark').\n"
        f"Consider writing style, character interactions, and any other relevant details.\n"
        f"**Just give 3 tones, separated by commas. e.g (\"Informative, Optimistic, Balanced\").\n"
        f"Do not make a sentence or add any other words/number.**\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"Chapter summaries:\n{context}"
    )
    
    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional book analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content

def build_keywords(synopsis, chapter_breakdown):
    print(f"[BUILD_KEYWORDS] Building keywords...")
    context = "\n".join([c["raw_output"] for c in chapter_breakdown[:3]])

    prompt = (
        f"Based on the synopsis and chapters below, identify 8 keywords that best represent the book.\n"
        f"Consider themes, and any other relevant details.\n"
        f"DO NOT INCLUDE CHARACTER NAMES.\n"
        f"**Just give 8 keywords in a list, separated by commas : Keyword1, Keyword2, .... Do not make a sentence or add any other words/number.**\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"Chapter summaries:\n{context}"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional book analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content

def build_1st_letter_thema_code(synopsis):
    prompt = (
        f"Your task is to assign the correct primary Thema code (only the first letter) to the following book, based on its synopsis.\n\n"
        f"Choose ONE of the following Thema codes:\n"
        f"A - The Arts\n"  
        f"C - Language and Linguistics\n" 
        f"D - Biography, Literature and Literary studies\n"  
        f"F - Fiction\n"  
        f"G - Reference, Information and Interdisciplinary subjects\n"  
        f"J - Society and Social Sciences\n"  
        f"K - Economics, Finance, Business and Management\n"  
        f"L - Law\n"  
        f"M - Medicine and Nursing\n"  
        f"N - History and Archaeology\n"  
        f"P - Mathematics and Science\n"  
        f"Q - Philosophy\n"  
        f"R - Earth Sciences, Geography, Environment, Planning\n"  
        f"S - Sports and Active outdoor recreation\n"  
        f"T - Technology, Engineering, Agriculture, Industrial processes\n"  
        f"U - Computing and Information Technology\n"  
        f"V - Health, Relationships and Personal development\n"  
        f"W - Lifestyle, Hobbies and Leisure\n"  
        f"X - Graphic novels, Comic books, Manga, Cartoons\n"  
        f"Y - Children’s, Teenage and Educational\n\n"
        f"Return ONLY the code (e.g. \"F\", \"Q\", etc.).\n"
        f"Here is the synopsis of the book:\n\n"
        f"{synopsis}"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a book classification assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content

def build_2nd_letter_thema_code(synopsis, prompt):
    prompt += synopsis
    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content

def build_comparison(synopsis, keywords):
    prompt = (
        f"Based on the synopsis and the keywords below, suggest 5 books that are similar in content, themes and audience.\n"
        f"Return the response in JSON format with the following structure:\n"
        f"[{{\"author\": \"Author Name\", \"title\": \"Book Title\", \"note\": \"Short note about the book\"}}, ...]\n\n"
        f"Synopsis:\n{synopsis}\n\n"
        f"Keywords:\n{keywords}\n\n"
    )
    
    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a book classification assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content