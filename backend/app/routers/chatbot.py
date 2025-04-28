# backend/app/routers/chat.py

from fastapi import APIRouter, Query
from sse_starlette.sse import EventSourceResponse
from backend.app.utils.rag.pipeline import answer_question_streaming

router = APIRouter()

@router.get("/chat/stream")
async def stream_chat(question: str = Query(...), book_id: str = Query(...)):
    async def event_generator():
        try:
            async for chunk in answer_question_streaming(book_id, question):
                yield {"data": chunk}
            yield {"event": "done", "data": "[DONE]"}
        except Exception as e:
            print("❌ LLM Streaming Error:", e)
            yield {"data": "An error occurred."}
    return EventSourceResponse(event_generator())
