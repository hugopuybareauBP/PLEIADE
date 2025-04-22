# backend/test/content/classification.py

import time 
import json
import re
import os

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

def build_primary_thema_code(synopsis):
    prompt = (
        f"Your task is to assign the correct primary Thema code (only the first letter) to the following book, based on its synopsis.\n\n"
        f"Choose ONE of the following Thema codes:\n"
        f"A - The Arts\n"  
        f"C - Language and Linguistics\n" 
        f"D - Biography, Literature and Literary studies\n"  
        f"F - Fiction\n"  
        f"G - Reference, Information and Interdisciplinary subjects\n"  
        f"J - Society and Social Sciences\n"  
        f"K - Economics, Finance, Business and Management\n"  
        f"L - Law\n"  
        f"M - Medicine and Nursing\n"  
        f"N - History and Archaeology\n"  
        f"P - Mathematics and Science\n"  
        f"Q - Philosophy\n"  
        f"R - Earth Sciences, Geography, Environment, Planning\n"  
        f"S - Sports and Active outdoor recreation\n"  
        f"T - Technology, Engineering, Agriculture, Industrial processes\n"  
        f"U - Computing and Information Technology\n"  
        f"V - Health, Relationships and Personal development\n"  
        f"W - Lifestyle, Hobbies and Leisure\n"  
        f"X - Graphic novels, Comic books, Manga, Cartoons\n"  
        f"Y - Children’s, Teenage and Educational\n\n"
        f"Return ONLY the code (e.g. \"F\", \"Q\", etc.).\n"
        f"Here is the synopsis of the book:\n\n"
        f"{synopsis}"
    )

    response = client.chat.completions.create(
            model=AZURE_OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a book classification assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=4096
        )

    return response.choices[0].message.content

# def parse_thema_code_output(raw_output):
#     match = re.match(r'\b([A-Z]{1,2})\b', raw_output.strip())
#     return match.group(1) if match else None

def get_secondary_thema_code_prompt(primary_thema_code):
    file_path = "backend/test/content/dumps/secondary_thema_prompts.json"
    try:
        with open(file_path, "r") as f:
            prompts = json.load(f)
        return prompts.get(primary_thema_code.strip().upper(), f"No prompt found for code '{primary_thema_code}'")
    except FileNotFoundError:
        return f"File '{file_path}' not found."
    except json.JSONDecodeError:
        return "Error reading JSON file. Please ensure it is properly formatted."
    
def build_secondary_thema_code(synopsis, primary_thema_code):
    prompt = get_secondary_thema_code_prompt(primary_thema_code)
    prompt += synopsis
    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content
     
if __name__ == "__main__":
    with open("backend/test/content/dumps/synopsis_echoes_2.json", "r") as f:
        data = json.load(f)
    synopsis = data["synopsis"]

    # with open("backend/test/summarization/summaries/alice_vivid_prompt_2.json", "r") as f:
    #         data = json.load(f)
    #         summaries = [summary["raw_output"] for summary in data["summary"]]

    start = time.time()
    print(f"Generating suggestion for primary Thema code...")
    primary_thema_code = build_primary_thema_code(synopsis)
    print(f"{primary_thema_code}")
    print(f"Execution time for primary thema code: {time.time() - start:.2f} seconds")
    start = time.time()
    print(f"Generating suggestion for secondary Thema code...")
    secondary_thema_code = build_secondary_thema_code(synopsis, primary_thema_code)
    print(f"{secondary_thema_code}")
    print(f"Execution time for secondary thema code: {time.time() - start:.2f} seconds")


