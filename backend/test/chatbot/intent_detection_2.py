# backend/tests/chatbot/intent_detection_2.py

import os

from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

# --- Azure OpenAI Configuration ---
api_version = "2024-12-01-preview"
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_INFERENCE_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_INFERENCE_ENDPOINT")
AZURE_OPENAI_MODEL_NAME = os.getenv("AZURE_OPENAI_INFERENCE_MODEL_NAME")

llm = AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=api_version,
    deployment_name=AZURE_OPENAI_MODEL_NAME,
    temperature=0.1,
    max_tokens=50
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

PLOT_CATEGORIES = { 
    "PLOT_BY_CHAPTER_X": "The user explicitly refers to a specific chapter number 'X'. Replace X with the number.",
    "PLOT_BY_POSITION_X": "The user refers to a part of the book. Replace X with 'beginning', 'middle', or 'end' according to the meaning of the query.",
    "PLOT_SEMANTIC": "The question is about plot content without reference to structure or position."
}

# --- Prompt Template ---
prompt_template = ChatPromptTemplate.from_template(
    """
    Classify the following user question into one of these categories:\n
    {categories}\n
    Respond with only the category name.\n
    Question: {question}
    """
)

intent_categories_text = "\n".join(f"{key}: {desc}" for key, desc in INTENT_CATEGORIES.items())
plot_categories_text = "\n".join(f"{key}: {desc}" for key, desc in PLOT_CATEGORIES.items())

intent_chain = prompt_template | llm | StrOutputParser()

def detect_intent(question: str) -> str:
    intent = intent_chain.invoke({"categories": intent_categories_text, "question": question}).strip()
    if intent == "PLOT":
        intent = intent_chain.invoke({"categories": plot_categories_text, "question": question}).strip()
    return intent

# --- CLI Test ---
if __name__ == '__main__':
    question = "Is this book good for children?"
    intent = detect_intent(question)
    print(f"Detected intent: {intent}")
