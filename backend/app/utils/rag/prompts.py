# backend/app/utils/rag/prompts.py

from langchain.prompts import ChatPromptTemplate
from typing import List, Dict

from backend.app.storage.storage import load_book_title

# --- Itent detection prompt template ---
intent_prompt_template = ChatPromptTemplate.from_template(
    """
    Classify the following user question into one of these categories:\n
    {categories}\n
    Respond with only the category name.\n
    Question: {question}
    """
)

# --- Chat prompt template ---
def build_chat_prompt(
        question: str,
        documents: list,
        book_id: str,
        history: List[Dict[str, str]]
    ) -> ChatPromptTemplate:

    messages = []

    # replay history
    if history:
        for msg in history:
            role = msg["role"]
            content = msg["content"]
            messages.append({"role": role, "content": content})

    # context layer
    context = "\n\n".join(doc.page_content for doc in documents)
    system_msg = {
        "role": "system",
        "content": (
            f"You are a helpful assistant for the book : {load_book_title(book_id)}. "
            "Use the following extracted context to answer the user:\n\n"
            f"{context}"
        )
    }
    messages.append(system_msg)

    # final user turn
    messages.append({"role": "user", "content": question})

    return ChatPromptTemplate.from_messages(messages)

