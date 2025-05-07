# backend/app/generation/llm.py

from typing import List
from backend.app.utils.details.llm_core import call_llm
from backend.app.utils.details.parsers import parse_model_json_response

### CHAPTER SUMMARIZATION ###

def summarize_chunk(chunk_text: str, chunk_id: int) -> dict:
    prompt = f"""
            You are a helpful assistant tasked with summarizing a passage from a book.

            1. Summarize the passage in a concise paragraph of approximately 100 words.
            2. Then suggest a short, relevant chapter title (max 8 words), based only on the content.
            3. Do NOT invent characters, places, or context. If the passage is too vague to name a title, return an empty string "" as the title.
            4. Your output must be a JSON object like this:
            {{
                "raw_output": "...",
                "suggested_title": "..."
            }}

            Here is the passage:
            ---
            {chunk_text}
            ---
            """
    content = call_llm("You are a helpful summarization assistant.", prompt)
    
    try:
        parsed = parse_model_json_response(content)
    except Exception:
        parsed = {
            "raw_output": content.strip(),
            "suggested_title": ""
        }

    return {
        "chapter_name": f"Chapter {chunk_id + 1}",
        "raw_output": parsed.get("raw_output", "").strip(),
        "suggested_title": parsed.get("suggested_title", "").strip()
    }

def build_chapter_breakdown(chunks) -> dict:
    return [summarize_chunk(chunk, i) for i, chunk in enumerate(chunks)]

def build_impact_analysis(chapter_breakdown) -> str:
    context = "\n".join([c["raw_output"] for c in chapter_breakdown])
    prompt = f"""
            Based on the chapter summaries below, write a list of 5 strengths and 5 weaknesses for this book.
            Focus on writing style, structure, clarity, examples, and depth of content.
            Respond with valid **minified JSON** ONLY. Do not include markdown, no explanations, no labels.
            Format:
            {{"strengths": ["..."], "weaknesses": ["..."]}}

            Chapter summaries:
            {context}
            """
    return call_llm("You are a professional book analyst.", prompt)

### CHARACTER GENERATION ###

def build_character_candidates_from_chunk(text: str) -> str:
    prompt = f"""
            Extract the full names of fictional characters explicitly mentioned in this book excerpt.
            Only include clearly named characters (no pronouns, vague roles, or invented names).
            Return as a bullet list.

            {text}
            """
    return call_llm("You are a professional literary analyst.", prompt)

def build_top_characters(unique_candidates: List[str], n: int = 10) -> str:
    prompt = f"""
            Here is a list of character names from a book:

            {chr(10).join(f"- {name}" for name in unique_candidates)}

            Clean this list by:
            - Merging duplicate names (e.g., 'The Hatter' and 'Mad Hatter')
            - Removing generic or non-informative entries
            - Returning at most {n} of the most important characters as a bullet list only.
            """
    return call_llm("You are a professional book analyst.", prompt)

def build_character_profile(character_name: str, context: str) -> str:
    prompt = f"""
            Write a concise character profile for {character_name} using only the information below.
            Return it as a JSON object like this:
            {{"character_name": "{character_name}", "description": "<context-based summary>"}}
            ---
            {context}
            ---
            """
    return call_llm("You are a literary analyst.", prompt, temperature=0.2)

### LOCATION GENERATION ###

def build_location_candidates_from_chunk(text: str) -> str:
    prompt = f"""
            Extract the names of fictional or real locations explicitly mentioned in this book excerpt.
            Include cities, buildings, landmarks, regions, and notable places. Exclude vague terms like 'the house' or 'the village'.
            Return them as a bullet list.

            {text}
            """
    return call_llm("You are a professional literary analyst.", prompt)

def build_top_locations(unique_locations: List[str], n: int = 10) -> str:
    prompt = f"""
            Here is a list of locations from a book:

            {chr(10).join(f"- {name}" for name in unique_locations)}

            Clean this list by:
            - Merging duplicate locations (e.g., 'Core chamber' and 'Core')
            - Removing generic or non-informative entries
            - Returning at most {n} of the most important locations as a bullet list only.
            """
    return call_llm("You are a professional book analyst.", prompt)

def build_location_note(location_name: str, context: str) -> str:
    prompt = f"""
            Write a short note about the location '{location_name}' using only the information below.
            Return it as a JSON object like this:
            {{"location_name": "{location_name}", "description": "<context-based summary>"}}
            ---
            {context}
            ---
            """
    return call_llm("You are a literary analyst.", prompt, temperature=0.2)

### MARKETING ###

def build_ecommerce_description(synopsis: str, title: str) -> str:
    prompt = f"""
            Here is a short synopsis of the book:
            {synopsis}

            Based on this, return a compelling and professional product description as a JSON object with this format:
            {{
              "description": ["A strong, attention-grabbing hook", "Followed by a few short, exciting sentences summarizing the book"],
              "bullets": ["Key takeaway 1", "Key takeaway 2", "Key takeaway 3"],
              "closing": "A persuasive sentence encouraging the user to buy the book."
            }}

            Make it exciting and accessible like something found on Amazon. Do NOT include markdown or explanations outside the JSON.
            """
    return call_llm("You are a professional copywriter creating an e-commerce book description.", prompt)

def build_tweet(synopsis: str) -> str:
    prompt = f"""
            Based on the following synopsis, generate a tweet that promotes the book.

            Synopsis:
            {synopsis}

            The tweet should be punchy, engaging, and fit within 280 characters. 
            Use a witty, modern tone. Finish with 3 different hashtags and don't mention AI or that it is based on a summary.
            """
    return call_llm("You are a social media content writer for a publishing house.", prompt, temperature=0.6)

def build_tiktok_script(synopsis: str) -> str:
    prompt = f"""
        Based on the following book synopsis, generate a TikTok video scenario lasting exactly 15 seconds.

        Synopsis:
        {synopsis}

        Return the scenario as a valid JSON object with the following structure:

        {{
            "title": "A short, engaging title for the video",
            "duration_seconds": 15,
            "segments": [
                {{
                    "start": 0,
                    "end": 3,
                    "narration": "Voiceover or text on screen",
                    "visuals": "What is shown on screen",
                    "sound": "Music or sound effect suggestion"
                }},
                {{
                    "start": 3,
                    "end": 6,
                    ...
                }}
                ...
            ],
            "call_to_action": "A final hook or CTA like 'Read to find out more!'"
        }}

        The tone should be fast-paced, modern, and BookTok-friendly.
        Prioritize grabbing attention in the first 3 seconds. 
        Don't mention AI or that this is based on a summary.
        Make sure your response is a valid JSON string, properly formatted.
    """
    return call_llm("You are a TikTok content writer for viral BookTok videos.", prompt, temperature=0.7)


### OVERVIEW & META ###

def build_synopsis(chapter_breakdown, title: str) -> str:
    context = "\n".join([c["raw_output"] for c in chapter_breakdown[:5]])
    prompt = f"""
            Book title: '{title}'

            Below are key points and chapter-level summaries extracted from the book:

            {context}

            Using ONLY this information, write a polished 2–3 sentence synopsis in the style of a book jacket blurb.
            - Capture the essence and themes of the book
            - Sound professional and high-level (not like a chapter summary)
            - Avoid bullet points and lists
            - Be suitable for an e-commerce product page or publisher's back cover
            - Do not mention summaries or chapters
            """
    return call_llm("You are a professional editor writing a short synopsis for a book.", prompt)

def build_time_period(synopsis, chapter_breakdown):
    context = "\n".join([c["raw_output"] for c in chapter_breakdown[:3]])
    prompt = f"""
            Based on the synopsis and chapters below, identify the time period covered by the book (e.g., 'Present day', '2030-2045', '19th century to now').
            Consider historical events, cultural references, and any other relevant details.
            The output should be maximum 10 words.

            Synopsis:
            {synopsis}

            Chapter summaries:
            {context}
            """
    return call_llm("You are a book publishing assistant.", prompt)

def build_genres(synopsis, chapter_breakdown):
    context = "\n".join([c["raw_output"] for c in chapter_breakdown[:5]])
    prompt = f"""
            Based on the synopsis and chapters below, identify the genres of the book (e.g., 'Science Fiction', 'Romance', 'Historical Fiction').
            **Just give 3 genres, separated by commas. e.g ("Technology, Business, Future Studies"). Do not make a sentence.**
            The first genre should be extracted from this list: 
                - Novel or Short Story: Fictional prose, the book is short, focusing on plot and character development.\n
                - Poetry: Literary work focused on the expression of feelings and ideas through rhythm, style, and metaphorical language.\n
                - Drama: A work intended for performance on stage, focusing on dialogue and action.\n
                - Essay: A short nonfiction text presenting an argument or personal reflection on a specific topic.\n
                - Autobiography / Memoir: A personal narrative written by the subject, recounting their own life or experiences.\n
                - Biography: A factual, third-person account of someone's life written by someone else.\n
                - Crime / Detective Fiction: Stories centered on solving a crime or mystery, often involving a detective or investigator.\n
                - Science Fiction: Speculative fiction involving futuristic science, technology, space, or other scientific elements.\n
                - Fantasy: Fiction set in imaginary worlds, often involving magic, mythical creatures, or supernatural events.\n
                - Historical Fiction: Fictional stories set in the past, often featuring real historical events or figures.\n\n

            Synopsis:
            {synopsis}

            Chapter summaries:
            {context}
            """
    return call_llm("You are a professional book analyst.", prompt)

def build_tone(synopsis, chapter_breakdown):
    context = "\n".join([c["raw_output"] for c in chapter_breakdown[:3]])
    prompt = f"""
            Based on the synopsis and chapters below, identify the tone of the book (e.g., 'Serious', 'Humorous', 'Dark').
            **Just give 3 tones, separated by commas. Do not make a sentence.**

            Synopsis:
            {synopsis}

            Chapter summaries:
            {context}
            """
    return call_llm("You are a professional book analyst.", prompt)

def build_keywords(synopsis, chapter_breakdown):
    context = "\n".join([c["raw_output"] for c in chapter_breakdown[:3]])
    prompt = f"""
            Based on the synopsis and chapters below, identify 8 keywords that best represent the book.
            **Just give 8 keywords in a list, separated by commas. Do NOT include character names.**

            Synopsis:
            {synopsis}

            Chapter summaries:
            {context}
            """
    return call_llm("You are a professional book analyst.", prompt)

def build_1st_letter(synopsis):
    prompt = f"""
            Your task is to assign the correct primary Thema code (only the first letter) to the following book, based on its synopsis.

            Choose ONE of the following Thema codes:
            A - The Arts, C - Language, D - Literature, F - Fiction, G - Reference, J - Society, K - Economics,
            L - Law, M - Medicine, N - History, P - Science, Q - Philosophy, R - Geography, S - Sports,
            T - Technology, U - Computing, V - Personal Development, W - Lifestyle, X - Graphic Novels, Y - Youth

            Return ONLY the code (e.g. "F", "Q", etc.).

            Here is the synopsis of the book:
            {synopsis}
            """
    return call_llm("You are a book classification assistant.", prompt)

def build_next_letter(synopsis, base_prompt):
    return call_llm("You are a book classification assistant.", base_prompt + synopsis)

def build_comparison(synopsis, keywords):
    prompt = f"""
            Based on the synopsis and the keywords below, suggest 5 books that are similar in content, themes and audience.
            Return the response in JSON format with the following structure:
            [{{"author": "Author Name", "title": "Book Title", "note": "Short note about the book"}}, ...]

            Synopsis:
            {synopsis}

            Keywords:
            {keywords}
            """
    return call_llm("You are a book classification assistant.", prompt)
