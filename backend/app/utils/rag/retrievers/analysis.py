# backend/app/utils/rag/retrievers/analysis.py

import json

from pathlib import Path
from typing import List

from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from backend.test.chatbot.rerankers.bge import rerank_bge

STORAGE_DIR = Path("backend/app/storage")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def analysis_retriever(book_id: str, question: str) -> List[Document]:
    book_path = STORAGE_DIR / "books" / f"book_{book_id}.json"
    with open(book_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    overview = data.get("overview", {})
    chapter_summaries = data.get("analysis", {}).get("chapters", [])

    content_blocks = []

    analysis = overview.get("contentAnalysis", {})
    if analysis:
        if "genres" in analysis:
            content_blocks.append(("Genres", analysis["genres"]))
        if "tone" in analysis:
            content_blocks.append(("Tone", analysis["tone"]))
        if "keywords" in analysis:
            content_blocks.append(("Keywords", ", ".join(analysis["keywords"])))
        if "timePeriod" in analysis:
            content_blocks.append(("Time Period", analysis["timePeriod"]))

    if "synopsis" in overview:
        content_blocks.append(("Synopsis", overview["synopsis"]))

    for ch in chapter_summaries:
        content_blocks.append((ch["chapter_name"], ch["raw_output"]))

    docs = [Document(page_content=f"{title}: {body}") for title, body in content_blocks]
    vectorstore = FAISS.from_documents(docs, embedding_model)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    return retriever.invoke(question)

