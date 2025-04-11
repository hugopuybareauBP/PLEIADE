# backend/test/content/character.py

import time
import json
import re

from ollama import chat

def generate_character_profile(character_name: str, context: str):
    prompt = (
        f"You are a literary analyst. Based on the context provided,"
        f"write a concise yet rich character profile for **{character_name}**.\n"
        f"Base your analysis only on the context provided.\n"
        f"---\n\n"
        f"{context}\n\n"
    )

    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

