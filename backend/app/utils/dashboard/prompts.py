# backend/app/utils/dashboard/prompts.py

from langchain.prompts import ChatPromptTemplate
from typing import List, Dict

spider_prompt_template = ChatPromptTemplate.from_template(
    """
    Rate the likelihood (0–100%) that this synopsis appeals to the following reader segments:\n
    - Young Adult (13–17)\n
    - New Adult (18–25)\n"
    - Adult (26–45)\n"
    - Mature (46+)\n\n"
    Respond in the exact format, one per line:\n"
    Young Adult (13–17): XX%\n"
    New Adult (18–25): XX%\n"
    Adult (26–45): XX%\n"
    Mature (46+): XX%\n\n"
    Synopsis: {text}"
    """
)

