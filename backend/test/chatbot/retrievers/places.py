# backend/test/chatbot/retrievers/places.py

import json
import time

from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

STORAGE_DIR = Path("backend/app/storage")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def load_places_retriever(book_id: str) -> FAISS:
    path = STORAGE_DIR / "books" / f"book_{book_id}.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    locations = data.get("analysis", {}).get("locations", [])

    docs = [
        Document(page_content=f"{loc['location_name']}: {loc['description']}")
        for loc in locations
        if "location_name" in loc and "description" in loc
    ]

    return FAISS.from_documents(docs, embedding_model)

if __name__ == "__main__":
    start = time.time()
    retriever = load_places_retriever("f7d67af3")
    results = retriever.similarity_search("Where does the trial take place?", k=3)
    for r in results:
        print(r.page_content)
    print(f"\nTime taken: {time.time() - start:.2f} seconds")
