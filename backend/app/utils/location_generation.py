# backend/app/utils/profile_generation.py

from typing import List

# LLM
from backend.app.utils.llm import build_location_candidates_from_chunk, build_top_locations, build_location_note
# Parsing
from backend.app.utils.parsers import parse_candidates, parse_top_candidates, parse_model_json_response
# Extraction
from backend.app.utils.extraction import extract_relevant_chunks

def get_all_location_candidates_from_book(book_chunks: List[str], chunk_group_size: int = 5) -> List[str]:
    all_candidates = []
    for i in range(0, len(book_chunks), chunk_group_size):
        grouped_text = "\n\n".join(book_chunks[i:i + chunk_group_size])
        print(f"\t📍 Processing location chunks {i}–{i + chunk_group_size - 1}")
        raw_output = build_location_candidates_from_chunk(grouped_text)
        candidates = parse_candidates(raw_output)
        all_candidates.extend(candidates)

    # Deduplicate while preserving order
    seen = set()
    return [x for x in all_candidates if not (x in seen or seen.add(x))]

def location_note_pipeline(chapter_breakdown) -> dict:
    print(f"[LOCATION_NOTE_PIPELINE] Starting location note pipeline")
    locations = []
    summaries = [c["raw_output"] for c in chapter_breakdown]
    print(f"[LOCATION_NOTE_PIPELINE] Summaries retrieved")
    unique_candidates = get_all_location_candidates_from_book(summaries)
    print(f"[LOCATION_NOTE_PIPELINE] Unique location candidates : {unique_candidates}")
    final_list = parse_top_candidates(build_top_locations(unique_candidates))
    print(f"[LOCATION_NOTE_PIPELINE] Final list of locations : {final_list}")
    print(f"[LOCATION_NOTE_PIPELINE] Starting location note generation")
    for loc in final_list[:5] if len(final_list) > 5 else final_list:
        print(f"\t Extracting relevant chunks for : {loc}")
        context = "\n\n".join(extract_relevant_chunks(summaries, loc, max_chunks=3))
        context = context.replace(loc, f"**{loc}**") # slightly better results
        locations.append(parse_model_json_response(build_location_note(loc, context)))
        print(f"[LOCATION_NOTE_PIPELINE] Location for {loc} correctly generated")

    return locations