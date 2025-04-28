# backend/tests/chatbot/intent_detection_2.py

from langchain.schema.output_parser import StrOutputParser

from backend.app.utils.rag.prompts import intent_prompt_template
from backend.app.utils.rag.llm import llm

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

intent_categories_text = "\n".join(f"{key}: {desc}" for key, desc in INTENT_CATEGORIES.items())
plot_categories_text = "\n".join(f"{key}: {desc}" for key, desc in PLOT_CATEGORIES.items())

intent_chain = intent_prompt_template | llm | StrOutputParser()

def detect_intent(question: str) -> str:
    intent = intent_chain.invoke({"categories": intent_categories_text, "question": question}).strip()
    if intent == "PLOT":
        intent = intent_chain.invoke({"categories": plot_categories_text, "question": question}).strip()
    return intent