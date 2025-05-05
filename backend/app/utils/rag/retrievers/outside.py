# backend/app/utils/rag/retrievers/outside.py

import json
from pathlib import Path
from typing import List

from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from backend.app.storage.storage import (
    load_book_title,
    load_book_author,
)

SOTRAGE_DIR = Path("backend/app/storage")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def outside_retriever(book_id: str, question: str) -> List[Document]:
    path = SOTRAGE_DIR / "books" / f"book_{book_id}.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    overview = data.get("overview", {})
    content_blocks = []

    # title/author or anything that could be useful for external context
    title = load_book_title(book_id)
    if title:
        content_blocks.append(("Title", title))
    author = load_book_author(book_id)
    if author:
        content_blocks.append(("Author", author))

    synopsis = overview.get("synopsis", "")
    if synopsis:
        content_blocks.append(("Synopsis", synopsis))

    for comparison in overview.get("comparison", []):
        title = comparison.get("title", "Unknown Title")
        author = comparison.get("author", "Unknown Author")
        note = comparison.get("note", "")
        content = f"{title} by {author} — {note}"
        content_blocks.append((f"Comparison: {title}", content))

    # Build documents
    docs = [Document(page_content=f"{title}: {content}") for title, content in content_blocks]

    # Create a temporary vectorstore and retriever
    vectorstore = FAISS.from_documents(docs, embedding_model)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    return retriever.invoke(question)
