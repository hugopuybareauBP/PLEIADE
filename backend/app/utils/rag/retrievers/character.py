# backend/app/utils/rag/retrievers/character.py

import json

from pathlib import Path
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

STORAGE_DIR = Path("backend/app/storage")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def character_retriever(book_id: str, question: str) -> List[Document]:
    path = STORAGE_DIR / "books" / f"book_{book_id}.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    character_data = data.get("analysis", {}).get("characters", [])
    docs = [
        Document(page_content=f"{char['character_name']}: {char['description']}")
        for char in character_data
        if "character_name" in char and "description" in char
    ]
    vectorstore = FAISS.from_documents(docs, embedding_model)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    return retriever.invoke(question)