# backend/app/utils/rag/prompts.py

from langchain.prompts import ChatPromptTemplate

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
def build_chat_prompt(question: str, documents: list, book_id: str) -> ChatPromptTemplate:
    context = "\n\n".join(doc.page_content for doc in documents)
    return ChatPromptTemplate.from_messages(
        [
            ("system", f"You are a helpful assistant that answers questions about the book {load_book_title(book_id)}."),
            ("system", f"Here is some helpful context considering the user's intent: {context}"),
            ("user", f"Now answer the following question: {question}"),
        ]
    )