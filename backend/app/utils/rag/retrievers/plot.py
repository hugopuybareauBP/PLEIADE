# backend/app/utils/rag/retrievers/plot.py

import json

from pathlib import Path
from typing import List

from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

from backend.app.utils.rag.rerankers.bge import rerank_bge

STORAGE_DIR = Path("backend/app/storage")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_chapter_summary(chapter_num: int, book_id) -> str:
    path = STORAGE_DIR / "books" / f"book_{book_id}.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    chapters = data.get("analysis", {}).get("chapters", [])
    for chapter in chapters:
        if chapter.get("chapter_name") == f"Chapter {chapter_num}":
            return chapter.get("raw_output", "")
    return ""

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

def plot_retriever_hybrid(book_id: str, query: str, top_k: int = 4) -> List[Document]:
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

def plot_retriever_by_chapter(book_id: str, intent: str) -> List[Document]:
    chapter_num = intent[-1]
    # print(f"Chapter number: {chapter_num}")
    summary = get_chapter_summary(chapter_num, book_id)
    return [Document(page_content=f"Chapter {chapter_num}: {summary}")] if summary else []

def plot_retriever_by_position(book_id: str, intent: str) -> List[Document]:
    summaries = _load_chapter_summaries(book_id)
    if not summaries:
        return []

    intent = intent.lower()
    n = len(summaries)

    if "beginning" in intent:
        selected = summaries[:2]
    elif "middle" in intent:
        selected = summaries[n//2 - 1:n//2 + 1] if n > 1 else summaries
    elif "end" in intent:
        selected = summaries[-2:]
    else:
        selected = []
    return selected

def plot_retriever(book_id: str, question: str, intent: str) -> List[Document]:
    if "PLOT_BY_CHAPTER" in intent :
        print(f"[PLOT_RETRIEVER] Intent: {intent}, Retrieving by chapter.")
        return plot_retriever_by_chapter(book_id, intent)
    elif "PLOT_BY_POSITION" in intent :
        print(f"[PLOT_RETRIEVER] Intent: {intent}, Retrieving by position.")
        return plot_retriever_by_position(book_id, intent)
    elif intent == "PLOT_SEMANTIC":
        print(f"[PLOT_RETRIEVER] Intent: {intent}, Retrieving with hybrid strategy.")
        initial_docs = plot_retriever_hybrid(book_id, question)
        reranked = rerank_bge(question, initial_docs, top_k=3)
        return reranked
    else:
        return []