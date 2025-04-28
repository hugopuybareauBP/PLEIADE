# backend/app/utils/rag/retrievers/__init__.py

from backend.app.utils.rag.retrievers.analysis import analysis_retriever
from backend.app.utils.rag.retrievers.character import character_retriever
from backend.app.utils.rag.retrievers.marketing import marketing_retriever
from backend.app.utils.rag.retrievers.places import places_retriever
from backend.app.utils.rag.retrievers.plot import plot_retriever

def retrieve_context(question: str, book_id: str, intent: str):
    if intent.startswith("CHARACTER"):
        return character_retriever(book_id, question)
    elif intent == "PLACES":
        return places_retriever(book_id, question)
    elif intent.startswith("PLOT"):
        return plot_retriever(book_id, question, intent)
    elif intent == "ANALYSIS":
        return analysis_retriever(book_id, question)
    elif intent == "MARKETING":
        return marketing_retriever(book_id, question)
    else:
        return []