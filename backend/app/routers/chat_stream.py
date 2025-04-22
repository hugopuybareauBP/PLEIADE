# backend/app/routers/chat_stream.py

from fastapi import APIRouter, Request, Query
from sse_starlette.sse import EventSourceResponse
from backend.app.utils.chatbot.llm import stream_gpt4o_response

router = APIRouter()

@router.get("/stream")
async def chat_stream(request: Request, question: str = Query(...), book_id: str = Query(None)):
    async def event_generator():
        async for chunk in stream_gpt4o_response(question, book_id=book_id):
            if await request.is_disconnected():
                break
            yield f"data: {chunk}\n\n"
    return EventSourceResponse(event_generator())

