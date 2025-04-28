# backend/app/utils/rag/retrievers/bge.py

from sentence_transformers import CrossEncoder
from langchain.docstore.document import Document
from typing import List

bge_reranker = CrossEncoder("BAAI/bge-reranker-base")

def rerank_bge(query: str, docs: List[Document], top_k: int = 4) -> List[Document]:
    if not docs:
        return []
    
    pairs = [(query, doc.page_content) for doc in docs]
    scores = bge_reranker.predict(pairs)

    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in ranked[:top_k]]