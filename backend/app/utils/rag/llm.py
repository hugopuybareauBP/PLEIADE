# backend/app/utils/chatbot/ask.py

import os

from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

# --- Azure OpenAI Configuration ---
api_version = "2024-12-01-preview"
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_MODEL_NAME = os.getenv("AZURE_OPENAI_MODEL_NAME")

llm = AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=api_version,
    deployment_name=AZURE_OPENAI_MODEL_NAME,
    temperature=0.1
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that answers questions about a book."),
        ("user", "{question}"),
    ]
)

chain = prompt | llm | StrOutputParser()