# backend/app/utils/rag/retrievers/places.py

import json

from pathlib import Path
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

STORAGE_DIR = Path("backend/app/storage")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def places_retriever(book_id: str, question: str) -> List[Document]:
    path = STORAGE_DIR / "books" / f"book_{book_id}.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    locations = data.get("analysis", {}).get("locations", [])
    docs = [
        Document(page_content=f"{loc['location_name']}: {loc['description']}")
        for loc in locations
        if "location_name" in loc and "description" in loc
    ]
    vectorstore = FAISS.from_documents(docs, embedding_model)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    return retriever.invoke(question)