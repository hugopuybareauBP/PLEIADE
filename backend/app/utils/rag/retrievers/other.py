# backend/app/utils/rag/retrievers/other.py

import json
from pathlib import Path
from typing import List

from langchain.docstore.document import Document

from backend.app.storage.storage import load_book_title

SOTRAGE_DIR = Path("backend/app/storage")

def other_retriever(book_id: str) -> List[Document]:
    title = load_book_title(book_id)

    fallback_message = (
        f"You were designed to answer questions on '{title}', "
        "You don't have enough context to answer this question right now."
    )

    return [Document(page_content=fallback_message)]