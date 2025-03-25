# backend/app/routers/spacy_stats.py

import os
import pandas as pd
import logging
import spacy

from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, HTTPException
from unidecode import unidecode

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

nlp = spacy.load("en_core_web_trf")

# Chunking
def chunk_text(text: str, max_tokens: int = 2000) -> List[str]:
    words = text.split()
    chunks = [" ".join(words[i:i + max_tokens]) for i in range(0, len(words), max_tokens)]
    return chunks

def process_text_to_docs(full_text: str) -> List[spacy.tokens.Doc]:

    chunks = chunk_text(full_text)
    doc_list = []
    for chunk in chunks:
        doc = nlp(chunk)
        doc_list.append(doc)

    return doc_list

# Feature extraction
def compute_features_from_docs(docs: List[spacy.tokens.Doc]) -> dict:

    total_tokens = 0
    total_sentences = 0
    pos_counts = {}
    entity_counts = {}

    for doc in docs:
        total_tokens += len(doc)
        total_sentences += len(list(doc.sents))

        # Part-Of-Speech (POS) counts
        for token in doc:
            pos_label = token.pos_
            pos_counts[pos_label] = pos_counts.get(pos_label, 0) + 1

        # Entity counts
        for ent in doc.ents:
            entity_label = ent.label_
            entity_counts[entity_label] = entity_counts.get(entity_label, 0) + 1

    avg_token_length = 0.0
    avg_sentence_length = 0.0

    if total_tokens > 0 and total_sentences > 0:
        # Average length of each token in characters
        total_characters = sum(len(token.text) for doc in docs for token in doc)
        avg_token_length = total_characters / total_tokens

        # Average number of tokens per sentence
        avg_sentence_length = total_tokens / total_sentences

    # Output dictionary
    features = {
        "total_tokens": total_tokens,
        "total_sentences": total_sentences,
        "avg_token_length": avg_token_length,
        "avg_sentence_length": avg_sentence_length,
    }

    # Merge POS and entity counts
    for pos_label, count in pos_counts.items():
        features[f"pos_{pos_label}_count"] = count

    for entity_label, count in entity_counts.items():
        features[f"entity_{entity_label}_count"] = count

    return features

def compute_features_from_docs_OPT(docs: List[spacy.tokens.Doc]) -> dict:
    total_tokens = 0
    total_sentences = 0
    total_characters = 0

    # Keep only a few relevant POS and entity types
    selected_pos = {"NOUN", "VERB", "PROPN"}
    selected_entities = {"PERSON", "GPE", "ORG"}

    pos_counts = {pos: 0 for pos in selected_pos}
    entity_counts = {ent: 0 for ent in selected_entities}

    for doc in docs:
        total_tokens += len(doc)
        total_sentences += len(list(doc.sents))
        total_characters += sum(len(token.text) for token in doc)

        for token in doc:
            if token.pos_ in selected_pos:
                pos_counts[token.pos_] += 1

        for ent in doc.ents:
            if ent.label_ in selected_entities:
                entity_counts[ent.label_] += 1

    avg_token_length = total_characters / total_tokens if total_tokens else 0.0
    avg_sentence_length = total_tokens / total_sentences if total_sentences else 0.0

    # Keep the output format compatible with the frontend
    features = {
        "total_tokens": total_tokens,
        "total_sentences": total_sentences,
        "avg_token_length": avg_token_length,
        "avg_sentence_length": avg_sentence_length,
    }

    for pos_label, count in pos_counts.items():
        features[f"pos_{pos_label}_count"] = count

    for entity_label, count in entity_counts.items():
        features[f"entity_{entity_label}_count"] = count

    return features

class TextPayload(BaseModel):
    filename: str
    full_text: str

@router.post("/spacy-stats")
async def extract_spacy_features(payload: TextPayload):
    doc_list = process_text_to_docs(payload.full_text)
    features = compute_features_from_docs_OPT(doc_list)
    return {"filename": payload.filename, "features": features}