# backend/app/utils/thema_code.py

from backend.app.utils.details.llm import build_1st_letter, build_next_letter
from backend.app.storage.storage import (
    get_2nd_letter_prompt,
    get_3rd_letter_prompt,
    get_thema_code_desc
)

def thema_code_pipeline(synopsis: str):
    first_letter = build_1st_letter(synopsis)
    print(f"[THEMA_CODE] First letter: {first_letter}")
    prompt_for_2nd_letter = get_2nd_letter_prompt(first_letter)
    second_letter = build_next_letter(synopsis, prompt_for_2nd_letter)
    print(f"[THEMA_CODE] Second letter: {second_letter}")
    primary_output = second_letter + " : " + get_thema_code_desc(second_letter)
    print(f"[THEMA_CODE] Primary output: {primary_output}")
    prompt_for_3rd_letter = get_3rd_letter_prompt(second_letter)
    third_letter = build_next_letter(synopsis, prompt_for_3rd_letter)
    print(f"[THEMA_CODE] Third letters: {third_letter}")
    code_values = [code.strip().upper() for code in third_letter.split(",")]
    secondary_results = []
    for code in code_values:
            secondary_results.append({
                "code": code,
                "label": get_thema_code_desc(code)
            })
    print(f"[THEMA_CODE] Secondary results: {secondary_results}")
    return primary_output, secondary_results