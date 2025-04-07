# backend/test/summarization/summarizer_4.py

import time
import os
import json

from ollama import chat

from backend.test.preprocessing.preprocessing_6 import preprocessing_pipeline

def summarize_chunk_with_mistral(chunk_text: str, chunk_id: int) -> dict:
    
    prompt = (
        f"Summarize the following book passage into a concise 100 word text.\n"
        f"- Skip any generic introduction or explanations about the book, chapter or the author.\n"
        f"- Focus on what happens, key characters, or any important developments.\n"
        f"- Write in a direct tone that sounds like a compelling recap, not like a school report.\n\n"
        f"{chunk_text}\n\n"
        f" Use vivid but concise language, think like a movie recap."
    )
    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "chunk_id": chunk_id,
        "raw_output": response["message"]["content"]
    }

def summarize_all_chunks(chunks) -> dict:

    summarized_chunks = []

    for id, chunk in enumerate(chunks):
        print(f"[INFO] Summarizing chunk {id}...")
        summary = summarize_chunk_with_mistral(chunk, id)
        summarized_chunks.append(summary)

    return {
        "summary": summarized_chunks
    }


if __name__ == "__main__":
    file_path = "backend/test/data/echoes.txt"
    with open(file_path, 'r') as f:
        dummy_text = f.read()

    for i in range(5):
        start_total = time.time()
        chunks = preprocessing_pipeline(dummy_text)
        # print(f"[PREPROCESSING] Preprocessing completed in {time.time() - start_total:.2f} seconds.")

        start_summarization = time.time()
        result = summarize_all_chunks(chunks)

        print(f"\n⚡ Summarization completed in {time.time() - start_summarization:.2f} seconds.")

    # for chapter, summary in enumerate(result["summary"]):
    #     print(f"=== CHAPTER {chapter} ===")
    #     print(summary)

    # filename = f"backend/test/summarization/summaries/echoes_3.json"
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    # with open(filename, "w") as f:
    #     json.dump(result, f, indent=4)
    # print(f"✅ Summaries saved to {filename}.\n")

