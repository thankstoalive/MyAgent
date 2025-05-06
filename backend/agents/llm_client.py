import os
import openai
from typing import List, Dict

# Initialize OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def call_chatgpt(messages: List[Dict[str, str]]) -> str:
    """
    Call OpenAI ChatCompletion API and return the assistant's message content.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.2,
    )
    return response.choices[0].message.content