# backend/test/cover_analysis/generate_cover.py

import torch
import json
import time
from datetime import datetime

from diffusers import StableDiffusionXLPipeline


device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

print(f"[COVER GENERATOR] Using device: {device}")

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16 if device != "cpu" else torch.float32,
    variant="fp16" if device != "cpu" else None
).to(device)

# pipe.enable_attention_slicing()

def create_prompt(synopsis_short: str, title: str = "PROJECT ECHO", authors: str = "By Blues & Amanda"):
    return f"""
    Professional cinematic book cover illustration for the book '{title}'.
    A realistic digital cover inspired by the following story: {synopsis_short}
    """

if __name__ == "__main__":
    with open("backend/test/content/dumps/synopsis_echoes_2.json", "r") as f:
        data = json.load(f)
        synopsis = data["synopsis"]
    
    synopsis_short = "A brilliant scientist uncovers a secret mind experiment while her identity merges with two allies. Together they must stop a hidden force threatening humanity."

    prompt = create_prompt(synopsis_short, title="PROJECT ECHO")

    start = time.time()
    print("[COVER GENERATOR] 🎨 Generating image, please wait...")
    image = pipe(prompt, num_inference_steps=40, guidance_scale=8.0).images[0]

    timestamp = datetime.now().strftime("%d_%H%M%S")
    image.save(f"backend/test/cover_analysis/generated/cover_{timestamp}.png")
    print(f"[COVER GENERATOR] Time taken: {time.time() - start:.2f} seconds")