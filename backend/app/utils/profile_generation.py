# backend/app/utils/profile_generation.py

from typing import List

# LLM
from backend.app.utils.llm import build_character_candidates_from_chunk, build_top_characters, build_character_profile
# Parsing
from backend.app.utils.parsers import parse_candidates, parse_top_candidates, parse_model_json_response
# Extraction
from backend.app.utils.extraction import extract_relevant_chunks

def get_all_character_candidates_from_book(book_chunks: List[str], chunk_group_size: int = 5) -> List[str]:
    all_candidates = []
    for i in range(0, len(book_chunks), chunk_group_size):
        grouped_text = "\n\n".join(book_chunks[i:i + chunk_group_size])
        print(f"\t🔍 Processing chunks {i}–{i + chunk_group_size - 1}")
        raw_output = build_character_candidates_from_chunk(grouped_text)
        candidates = parse_candidates(raw_output)
        all_candidates.extend(candidates)

    # Deduplicate while preserving order
    seen = set()
    return [x for x in all_candidates if not (x in seen or seen.add(x))]
    
def profile_generation_pipeline(chapter_breakdown) -> dict:
    print(f"[PROFILE_GENERATION_PIPELINE] Starting profile generation pipeline")
    profiles = []
    summaries = [c["raw_output"] for c in chapter_breakdown]
    print(f"[PROFILE_GENERATION_PIPELINE] Summaries retrieved")
    unique_candidates = get_all_character_candidates_from_book(summaries)
    print(f"[PROFILE_GENERATION_PIPELINE] Unique candidates : {unique_candidates}")
    final_list = parse_top_candidates(build_top_characters(unique_candidates))
    print(f"[PROFILE_GENERATION_PIPELINE] Final list of characters : {final_list}")
    print(f"[PROFILE_GENERATION_PIPELINE] Starting profile generation")
    for char in final_list[:7] if len(final_list) > 7 else final_list:
        print(f"\t Extracting relevant chunks for : {char}")
        context = "\n\n".join(extract_relevant_chunks(summaries, char, max_chunks=3))
        context = context.replace(char, f"**{char}**") # slightly better results
        profiles.append(parse_model_json_response(build_character_profile(char, context)))
        print(f"[PROFILE_GENERATION_PIPELINE] Profile for {char} correctly generated")

    return profiles