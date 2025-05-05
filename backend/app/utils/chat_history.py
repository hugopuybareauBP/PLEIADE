# backend/app/utils/chat_history.py

from pathlib import Path
from typing import Dict, List

from langchain.memory.chat_message_histories import FileChatMessageHistory
from langchain.schema import AIMessage, HumanMessage

CHAT_DIR = Path("backend/app/storage/chat_history")
CHAT_DIR.mkdir(parents=True, exist_ok=True)

def _get_history_obj(book_id: str) -> FileChatMessageHistory:
    return FileChatMessageHistory(str(CHAT_DIR / f"session_{book_id}.json"))

def get_history(book_id: str) -> List[Dict[str, str]]:
    history = _get_history_obj(book_id).messages
    result = []
    for msg in history:
        if isinstance(msg, HumanMessage):
            result.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            result.append({"role": "assistant", "content": msg.content})
    return result

def add_user_message(book_id: str, content: str) -> None:
    _get_history_obj(book_id).add_user_message(content)

def add_assistant_message(book_id: str, content: str) -> None:
    _get_history_obj(book_id).add_ai_message(content)

def clear_history(book_id: str) -> None:
    path = CHAT_DIR / f"session_{book_id}.json"
    if path.exists():
        path.unlink()
