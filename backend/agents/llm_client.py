import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict

# Load environment variables from .env file, then initialize OpenAI client
load_dotenv()
_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_chatgpt(
    messages: List[Dict[str, str]],
    model: str = "gpt-4o-mini",
    temperature: float = 0.2,
) -> str:
    """
    Call OpenAI Chat Completion API and return the assistant's message content.
    """
    # Use the OpenAI Python v1 client interface
    response = _client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # Simple test when running this module directly
    from dotenv import load_dotenv
    load_dotenv()  # load OPENAI_API_KEY from .env if present
    # Example messages
    test_messages = [
        {"role": "system",  "content": "You are a helpful assistant."},
        {"role": "user",    "content": "Hello, world!"},
    ]
    # Call the API and print the response (with error handling)
    try:
        reply = call_chatgpt(test_messages)
        print("Assistant reply:", reply)
    except Exception as err:
        print("Error during ChatGPT API call:", err)