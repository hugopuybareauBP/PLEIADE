# backend/test/cover_analysis/generate_cover_2.py

import os 
import base64
import json
import time

from openai import AzureOpenAI

# Azure OpenAI Configuration
api_version = "2024-12-01-preview"
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_IMAGE_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_IMAGE_ENDPOINT")
AZURE_OPENAI_MODEL_NAME = os.getenv("AZURE_OPENAI_IMAGE_MODEL_NAME")  # e.g. "dalle-3"

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=api_version,
)

def generate_cover(synopsis: str, author: str, title: str):
    prompt = f"""
    A flat, front-facing digital illustration of a book cover.

    Title: "{title}"
    Author: {author}

    Use the following synopsis as inspiration for the visual design of the cover (but do not include any of this text in the image):

    {synopsis}

    Instructions:
    - Only generate the front cover artwork — do not show the book as a physical object.
    - Do not add any fake or unreadable text or taglines.
    - Do not render the spine or back cover.
    - Typography should be minimal, clean, and legible.
    - The overall design should reflect the tone and themes of the synopsis.
    """


    response = client.images.generate(
        model=AZURE_OPENAI_MODEL_NAME,
        prompt=prompt,
        n=1,
        size="1024x1024", # "1024x1024" in prod
        quality="standard", # "hd" in prod
        style="vivid",
        response_format="b64_json"
    )

    return response.data[0].b64_json

if __name__ == "__main__":
    with open("backend/test/content/dumps/synopsis_echoes_2.json", "r") as f:
        data = json.load(f)
        synopsis = data["synopsis"]
    
    author = "ChatGPT"
    title = "PROJECT ECHO"

    start = time.time()
    print("[COVER GENERATOR] 🎨 Generating image, please wait...")
    image_b64 = generate_cover(synopsis, author, title)

    timestamp = time.strftime("%d_%H%M%S")
    with open(f"backend/test/cover_analysis/generated/cover_{timestamp}.png", "wb") as img_file:
        img_file.write(base64.b64decode(image_b64))
    
    print(f"[COVER GENERATOR] Time taken: {time.time() - start:.2f} seconds")