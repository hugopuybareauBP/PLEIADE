# backend/app/utils/rag/retrievers/marketing.py

import json 

from pathlib import Path
from typing import List

from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

SOTRAGE_DIR = Path("backend/app/storage")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def marketing_retriever(book_id: str, question: str) -> List[Document]:    
    path = SOTRAGE_DIR / "books" / f"book_{book_id}.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    overview = data.get("overview", {})
    content_blocks = []

    if "synopsis" in overview:
        content_blocks.append(("Synopsis", overview["synopsis"]))

    key_data = overview.get("key_data", {})
    if key_data:        
        key_data_text = "\n".join(f"{k}: {v}" for k, v in key_data.items())
        content_blocks.append(("Key Data", key_data_text))
    
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

    for comparison in overview.get("comparison", []):
        title = comparison.get("title", "Unknown Title")
        author = comparison.get("author", "Unknown Author")
        # note = comparison.get("note", "")
        content = f"{title} by {author}"
        content_blocks.append((f"Comparison: {title}", content))

    docs = [Document(page_content=f"{title}: {content}") for title, content in content_blocks]
    vectorstore = FAISS.from_documents(docs, embedding_model)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    return retriever.invoke(question)