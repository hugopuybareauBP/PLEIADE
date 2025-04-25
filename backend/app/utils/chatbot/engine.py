# backend/app/utils/chatbot/engine.py

# from backend.app.utils.chatbot.intent_detection import detect_intent
# from backend.app.utils.chatbot.retrieval import retrieve_context_chunks
# from backend.app.utils.chatbot.reranker import rerank_chunks
# from backend.app.utils.chatbot.prompt_builder import build_prompt
# from backend.app.utils.llm import ask_gpt4o  # assumes Azure OpenAI call wrapper

def run_chatbot_pipeline(book_id: str, question: str) -> str:
    # Step 1: Detect intent
    # intent = detect_intent(question)

    # Step 2: Retrieve context based on intent
    # raw_chunks = retrieve_context_chunks(book_id=book_id, question=question, intent=intent)

    # Step 3: Rerank and truncate
    # top_chunks = rerank_chunks(question, raw_chunks, top_n=3)

    # Step 4: Build prompt
    # prompt = build_prompt(book_id, top_chunks, question)

    # Step 5: Query the LLM
    # answer = ask_gpt4o(prompt)

    return "answer"
