# backend/app/utils/cover_analysis/cover_analysis.py

import os
import json
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

def analyze_cover(base64_image: str, temperature: float = 0.3, max_tokens: int = 1000) -> dict:
    user_prompt = """
    You are an expert in visual design and editorial storytelling.
    I will send you the image of a book cover.

    Your task is to analyze the visual and textual content of the cover and break it down into four key narratives or design elements that define what the cover is “talking about.”

    Return a JSON array where each element contains:
    - "category": a concise label like "Hero Story", "Emotional Tribute", or "Masthead & Furniture"
    - "title": a short quoted text taken or inferred from the cover (e.g. a headline or key phrase)
    - "description": 1-2 sentence summary of the meaning, aesthetic, or emotional role of the element
    - "icon": an emoji that matches the theme (🔥 for drama, ❤️ for romance, 🧠 for intellect, 🖼️ for art, etc.)

    Do not include any emojis or markdown. Return raw valid JSON only.
    """

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ],
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    raw_output = response.choices[0].message.content

    try:
        return json.loads(raw_output)
    except Exception as e:
        return {
            "error": "Invalid JSON response",
            "raw_output": raw_output,
            "exception": str(e)
        }
