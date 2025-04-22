# backend/app/utils/chatbot/intent_detection.py

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

def detect_intent(question: str) -> str:
    prompt = (
        f"Classify the following question into one of the following intents:\n\n"
        f"1. CHARACTER\n"
        f"2. PLOT\n"
        f"3. AGE\n"
        f"4. MARKETING\n"
        f"5. OTHER\n"
        f"\nQuestion: {question}\n"
        f"Only return the intent number (1-5) without any additional text."
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a classification assistant for in intent detection in a chatbot."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=3
    )

    return response.choices[0].message.content.strip()



