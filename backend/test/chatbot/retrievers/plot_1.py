# backend/test/chatbot/retrievers/plot.py

import json
import time

from pathlib import Path
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

STORAGE_DIR = Path("backend/app/storage")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def _load_chapter_summaries(book_id: str) -> List[Document]:
    path = STORAGE_DIR / "books" / f"book_{book_id}.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chapters = data.get("analysis", {}).get("chapters", [])

    return [
        Document(page_content=f"{c["chapter_name"]}: {c["raw_output"]}")
        for c in chapters
        if "chapter_name" in c and "raw_output" in c
    ]

def _load_plot_chunks(book_id: str) -> List[Document]:
    path = STORAGE_DIR / "books_overview.json"
    with open(path, "r", encoding="utf-8") as f:
        books = json.load(f)

    book = next((b for b in books if b.get("id") == book_id), None)
    if not book or "chunks" not in book:
        return []
    return [
    Document(page_content=f"Chapter {chunk['chunk_id'] + 1}: {chunk['chunk_text']}")
        for chunk in book["chunks"]
        if "chunk_text" in chunk
    ]

def load_hybrid_plot_context(book_id: str, query: str, top_k: int = 4) -> List[Document]:
    # load both sources
    summaries = _load_chapter_summaries(book_id)
    plot_chunks = _load_plot_chunks(book_id)

    all_docs = summaries + plot_chunks

    # embed everything
    query_embedding = embedding_model.embed_query(query)
    doc_embeddings = embedding_model.embed_documents([doc.page_content for doc in all_docs])

    # compute cosine similarity manually because FAISS cant handle cross source merging
    # import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity

    sims = cosine_similarity([query_embedding], doc_embeddings)[0]
    top_indices = sims.argsort()[::-1][:top_k]

    return [all_docs[i] for i in top_indices]

if __name__ == "__main__":
    docs = load_hybrid_plot_context("f7d67af3", "What happens at the start of the book?", top_k=3)
    for doc in docs:
        print(doc.page_content)
