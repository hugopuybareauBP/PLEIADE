# backend/app/utils/extraction.py

import torch

from sentence_transformers import SentenceTransformer, util
from typing import List

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_relevant_chunks(chunks: List[str], location_name: str, max_chunks: int = 5) -> List[str]:
    chunk_embeddings = embedding_model.encode(chunks, convert_to_tensor=True)
    query_embedding = embedding_model.encode(location_name, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_embedding, chunk_embeddings)[0]
    top_results = torch.topk(cosine_scores, k=min(max_chunks, len(chunks)))
    return [chunks[idx] for idx in top_results.indices]