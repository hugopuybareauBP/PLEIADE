# backend/test/chatbot/intent_detection.py

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

INTENT_CATEGORIES = {
    "CHARACTER": "Questions about specific characters, their names, roles, relationships, personalities, or development arcs. Example: 'Is Alice the sister of Bob?' or 'Who is the main villain?'",
    "PLACES": "Questions about locations, settings, and environments in the story. Includes both real and fictional places. Example: 'Where does the story take place?' or 'What is the significance of the Whispering Woods?'",
    "PLOT": "Direct, factual questions about the main storyline or events that happen in the book. Typically limited in scope. Example: 'What happens in chapter 3?' or 'How does the book end?'",
    "ANALYSIS": "Interpretive or reflective questions that require broader understanding of the themes, symbols, structure, or deeper meanings in the book. Example: 'What is the author's message about grief?' or 'How does the protagonist’s journey reflect existential themes?'",
    "MARKETING": "Questions related to how the book is pitched, its emotional tone, target audience, or genre fit. Example: 'Is this book good for fans of fantasy?' or 'What’s the elevator pitch of the story?'",
    "OUTSIDE": "Questions requiring knowledge beyond the book’s content, such as author biography, cultural context, comparisons with other works, or real-world facts. Example: 'Was this inspired by World War II?' or 'What books are similar to this one?'",
    "OTHER": "Questions that do not fit into the above categories or cannot be answered due to lack of context or relevance."
}

def detect_intent(question: str) -> str:
    prompt = (
        f"Classify the following user question into one of these categories:"
        f"{chr(10).join(f"{key}: {desc}" for key, desc in INTENT_CATEGORIES.items())}\n"
        f"Respond with only the category name.\n"
        f"Question: {question}\n"
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
    
    return response.choices[0].message.content

if __name__ == '__main__':
    # question = "What is the main character's motivation in the story?"
    question = "What is the purpose of Paul in the story?"
    intent = detect_intent(question)
    print(f"Detected intent: {intent}")