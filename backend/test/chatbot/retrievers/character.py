# backend/test/chatbot/retrievers/character.py

import json
import time

from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

STORAGE_DIR = Path("backend/app/storage")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def load_character_retriever(book_id: str) -> FAISS:
    path = STORAGE_DIR / "books" / f"book_{book_id}.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    character_data = data.get("analysis", {}).get("characters", [])
    docs = [
        Document(page_content=f"{char['character_name']}: {char['description']}")
        for char in character_data
        if "character_name" in char and "description" in char
    ]

    return FAISS.from_documents(docs, embedding_model)

if __name__ == "__main__":
    start = time.time()
    retriever = load_character_retriever("f7d67af3")
    results = retriever.similarity_search("Who is Alice?", k=2)
    for r in results:
        print(r.page_content)
    print(f"\nTime taken: {time.time() - start:.2f} seconds")
