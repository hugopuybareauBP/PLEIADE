# backend/test/summarization/azure.py

import time
import os
import json

from openai import AzureOpenAI

from backend.test.preprocessing.preprocessing_8 import preprocessing_pipeline

# Azure OpenAI Configuration
api_version = "2024-12-01-preview"
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_MODEL_NAME = os.getenv("AZURE_OPENAI_MODEL_NAME")

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=api_version,
)

def summarize_chunk_with_gpt4o(chunk_text: str, chunk_id: int) -> dict:
    prompt = (
        f"Summarize the following book passage into a concise 100 word text.\n"
        f"- Skip any generic introduction or explanations about the book, chapter or the author.\n"
        f"- Focus on what happens, key characters, or any important developments.\n"
        f"- Summarize this chapter based only on the provided text.\n"
        f"- Do not invent characters or settings. If the text is vague, keep the summary general.\n\n"
        f"{chunk_text}"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful summarization assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return {
        "chunk_id": chunk_id,
        "raw_output": response.choices[0].message.content
    }

def summarize_all_chunks(chunks) -> dict:
    summarized_chunks = []
    for id, chunk in enumerate(chunks):
        print(f"[INFO] Summarizing chunk {id}...")
        summary = summarize_chunk_with_gpt4o(chunk, id)
        summarized_chunks.append(summary)
    return {"summary": summarized_chunks}


if __name__ == "__main__":
    file_path = "backend/test/data/Echoes.txt"
    with open(file_path, 'r') as f:
        dummy_text = f.read()

    start_total = time.time()
    chunks = preprocessing_pipeline(dummy_text)
    print(f"[PREPROCESSING] Preprocessing completed in {time.time() - start_total:.2f} seconds.")

    start_summarization = time.time()
    result = summarize_all_chunks(chunks)

    print(f"\n⚡ Summarization completed in {time.time() - start_summarization:.2f} seconds.")

    # for chapter, summary in enumerate(result["summary"]):
    #     print(f"=== CHAPTER {chapter} ===\n\n")
    #     print(f"Summary : {summary}\n")
    #     print(f"Chunk built on : {chunks[chapter]}\n")

    filename = "backend/test/summarization/summaries/echoes_azure_1.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(result, f, indent=4)
    print(f"✅ Summaries saved to {filename}.\n")