from vllm import LLM
from transformers import AutoTokenizer
from huggingface_hub import login

login("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")

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
llm = LLM(model=MODEL_NAME, device="cpu")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

messages = [
    {"role": "user", "content": "Summarize the French Revolution in 3 bullet points."}
]
prompt = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)

outputs = llm.generate(prompt, max_tokens=256)
print(outputs[0].outputs[0].text)
