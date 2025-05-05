# backend/test/preprocessing/preprocessing_9.py*

import time
import os
import pdfplumber
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

def extract_first_pages(pdf_path: str, max_pages: int = 10) -> str:
    extracted_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[:max_pages]:
            extracted_text.append(page.extract_text() or "")
    return "\n\n".join(extracted_text)

def detect_TOC(text: str) -> str:
    prompt = f"""
            You are a Table of Contents extractor.

            Given the following text extracted from the beginning of a book, determine if it contains a Table of Contents (ToC).

            If it does, output a clean list of the chapters you see in the TOC and their page numbers in JSON format like this:

            [
                {{"title": "Chapter 1: The Beginning", "page": 1}},
                {{"title": "Chapter 2: A Strange Encounter", "page": 10}}
            ]

            If information is missing for any chapter (title or page number), fill it with an empty string ("") instead of inventing content.

            If there is no Table of Contents, respond exactly with the string "NO_TOC".

            Here is the text:
            ---
            {text}
            ---
            """
    
    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a Table of Contents extractor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=1500
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    start = time.time()
    pdf_path = "backend/test/data/PROJECT ECHO.pdf"
    extracter_test = extract_first_pages(pdf_path)
    print(f"Extracted text: {extracter_test}")
    # toc = detect_TOC(extracter_test)
    # print(f"Detected ToC: {toc}")
    print(f"Time taken to extract text: {time.time() - start:.2f} seconds")