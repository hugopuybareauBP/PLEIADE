# backend/app/utils/thema_code.py

import json

from backend.app.utils.llm import build_1st_letter_thema_code, build_2nd_letter_thema_code
from backend.app.storage.storage import get_2nd_letter_thema_code_prompt, get_thema_code_desc

def thema_code_pipeline(synopsis: str):
    # first letter
    first_letter = build_1st_letter_thema_code(synopsis)
    # second letter
    print(f"[THEMA_CODE] First letter: {first_letter}")
    prompt_for_2nd_letter = get_2nd_letter_thema_code_prompt(first_letter)
    primary_thema_code = build_2nd_letter_thema_code(synopsis, prompt_for_2nd_letter)
    print(f"[THEMA_CODE] Primary thema code: {primary_thema_code}")
    final = primary_thema_code + " : " + get_thema_code_desc(primary_thema_code)
    print(f"[THEMA_CODE] Final thema code: {final}") 
    return final