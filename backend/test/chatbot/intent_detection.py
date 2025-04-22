#backend/test/chatbot/intent_detection.py

import os

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

INTENT_CATEGORIES = [
    "CHARACTER", # related to specific characters
    "PLACES", # questions about places
    "PLOT", # general questions about the plot
    "ANALYSIS", # question about the plot that might necessitate a wider retrieval than "PLOT"
    "MARKETING", # marketing-related questions
    "OUTSIDE", # question that necessitate information outside of the book
    "OTHER", # to return an retrieval error
]

def detect_intent(question: str) -> str:
    prompt = (
        f"Classify the following user question into one of the categories:"
        f"{", ".join(INTENT_CATEGORIES)}."
        f"Respond with only the category name."
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You classify queries of users to manage a retrieval system."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=50
    )