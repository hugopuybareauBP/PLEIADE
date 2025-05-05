# backend/app/routers/chatbot.py

from fastapi import APIRouter, Query, HTTPException
from sse_starlette.sse import EventSourceResponse

from backend.app.utils.rag.pipeline import answer_question_streaming
from backend.app.utils.chat_history import (
    add_user_message,
    add_assistant_message,
    get_history,
    clear_history
)

router = APIRouter()

@router.get("/chat/stream")
async def stream_chat(question: str = Query(...), book_id: str = Query(...)):
    add_user_message(book_id, question)
    async def event_generator():
        full_answer = ""
        try:
            async for chunk in answer_question_streaming(book_id, question):
                full_answer += chunk
                yield {"data": chunk}
            yield {"event": "done", "data": "[DONE]"}
        except Exception as e:
            print("❌ LLM Streaming Error:", e)
            yield {"data": "An error occurred."}
        finally:
            add_assistant_message(book_id, full_answer)

    return EventSourceResponse(event_generator())

@router.get("/chat/history")
async def chat_history(book_id: str = Query(...)):
    return {"history": get_history(book_id)}

@router.delete("/chat/history")
async def delete_chat_history(book_id: str = Query(...)):
    try:
        clear_history(book_id)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not clear history")