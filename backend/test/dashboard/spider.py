# backend/test/dashboard/spider.py

import os
import json
import math
import matplotlib
matplotlib.use("TkAgg")  # Use TkAgg backend for matplotlib
import matplotlib.pyplot as plt

import time

from openai import AzureOpenAI

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

def get_audience_scores(text: str) -> dict:
    prompt = (
        f"Rate the likelihood (0–100%) that this synopsis appeals to the following reader segments:\n"
        f"- Young Adult (13–17)\n"
        f"- New Adult (18–25)\n"
        f"- Adult (26–45)\n"
        f"- Mature (46+)\n\n"
        f"Respond in the exact format, one per line:\n"
        f"Young Adult (13–17): XX%\n"
        f"New Adult (18–25): XX%\n"
        f"Adult (26–45): XX%\n"
        f"Mature (46+): XX%\n\n"
        f"Synopsis: {text}"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You classify queries of users to manage a retrieval system."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=500
    )
    
    content = response.choices[0].message.content
    scores = {}
    for line in content.splitlines():
        if ":" in line:
            seg, pct = line.split(":", 1)
            scores[seg.strip()] = float(pct.strip().rstrip("%"))
    return scores

if __name__ == "__main__":
    start = time.time() 
    with open("backend/test/content/dumps/synopsis_alice.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    synopsis = data["synopsis"]
    audience_scores = get_audience_scores(synopsis)
    labels = list(audience_scores.keys())
    values = list(audience_scores.values())
    values += values[:1]  # close the loop
    angles = [n / float(len(labels)) * 2 * math.pi for n in range(len(labels))]
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticks([0,20,40,60,80,100])
    ax.set_yticklabels(["0%","20%","40%","60%","80%","100%"])
    ax.set_title("Target Reader Segmentation", y=1.1)
    plt.tight_layout()
    plt.show()
    print(f"Time elapsed: {time.time() - start:.2f} seconds")