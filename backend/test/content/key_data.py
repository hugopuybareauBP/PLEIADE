# backend/test/content/key_data.py

import time
import spacy
import math
import json

nlp = spacy.load("en_core_web_sm")

def extract_key_data(text: str, chapter_breakdown) -> dict:
    # Key data 
    total_words = len(text.split())
    reading_minutes = total_words/250 
    hours = int(reading_minutes / 60)
    minutes = int(reading_minutes % 60)
    estimated_reading_time = f"{hours}h {minutes}m" if hours > 0 else f"{minutes} minutes"
    estimated_pages = math.ceil(total_words / 250)
    chapter_count = len(chapter_breakdown)

    # NLP analysis
    doc = nlp(text)
    people = list({ent.text for ent in doc.ents if ent.label_ == "PERSON"})
    locations = list({ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]})    

    # output
    key_data = {
        "estimatedReadingTime": estimated_reading_time,
        "wordCount": f"{total_words} words",
        "pages": f"{estimated_pages} pages",
        "chapters": f"{chapter_count} chapters",
        "Total characters": f"{len(people)} characters mentioned",
        "keyLocations": f"{len(locations)} locations mentioned",
    }

    return key_data

if __name__ == "__main__":
    start = time.time()
    with open("backend/test/data/echoes.txt", "r", encoding="utf-8") as file:
        text = file.read()

    with open("backend/test/summarization/summaries/echoes_3.json", "r", encoding="utf-8") as file:
        chapter_breakdown = json.load(file)

    key_data = extract_key_data(text, chapter_breakdown)
    print(f"Generated key_data in {time.time() - start:.2f} seconds.\n\n")
    print(key_data)