# backend/app/utils/rag/pipeline.py

from langchain_core.output_parsers import StrOutputParser

from backend.app.utils.rag.intent import detect_intent
from backend.app.utils.rag.dispatcher import retrieve_context
from backend.app.utils.rag.llm import llm
from backend.app.utils.rag.prompts import build_chat_prompt

from backend.app.utils.chat_history import get_history

async def answer_question_streaming(book_id: str, question: str):
    print(f"[CHATBOT] New user query : {question}")
    intent = detect_intent(question)
    print(f"    [INTENT_DETECTION] Detected intent : {intent}")
    docs = retrieve_context(question, book_id, intent)
    print(f"    [RETRIEVAL] Retrieved {len(docs)} documents.")
    history = get_history(book_id)
    print(f"    [CHAT_HISTORY] Loaded {len(history)} previous messages.")
    prompt = build_chat_prompt(question, docs, book_id, history)
    print(f"    [PROMPT] Final build for prompt : {prompt}")

    chain = prompt | llm | StrOutputParser()
    async for chunk in chain.astream({}):
        yield chunk