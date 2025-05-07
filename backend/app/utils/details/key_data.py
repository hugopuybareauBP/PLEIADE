# backend/app/utils/details/key_data.py

import spacy

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 10_000_000

def build_key_data(text: str, chapter_breakdown, pages) -> dict:
    # Key data 
    total_words = len(text.split())
    reading_minutes = total_words/250 
    hours = int(reading_minutes / 60)
    minutes = int(reading_minutes % 60)
    estimated_reading_time = f"{hours}h {minutes}m" if hours > 0 else f"{minutes} minutes"
    chapter_count = len(chapter_breakdown)

    # NLP analysis
    doc = nlp(text)
    people = list({ent.text for ent in doc.ents if ent.label_ == "PERSON"})
    locations = list({ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]})    

    # output
    key_data = {
        "estimatedReadingTime": estimated_reading_time,
        "wordCount": f"{total_words} words",
        "pages": f"{pages} pages",
        "chapters": f"{chapter_count} chapters",
        "mainCharacters": f"{len(people)} characters mentioned",
        "keyLocations": f"{len(locations)} locations mentioned",
    }

    return key_data