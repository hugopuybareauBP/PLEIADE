# backend/app/utils/chatbot/ask.py

import os
import asyncio

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

def ask_gpt4o_mini(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in ask_gpt4o_mini: {e}")
        return "Error asking the model. Refresh the page and try again."
    
async def stream_gpt4o_response(prompt: str, book_id: str = None):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    for chunk in response:
        # ensure choice exists
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta
        if hasattr(delta, "content") and delta.content:
            yield delta.content