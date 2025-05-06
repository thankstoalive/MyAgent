from typing import Any, Dict
from backend.models.chat_state import ChatState
from backend.agents.llm_client import call_chatgpt

def respond_node(state: ChatState) -> ChatState:
    """
    Generate a user-facing response based on the filesystem operation result.
    Appends the assistant message to state['history'].
    """
    fs_output = state.get("fs_result", "")
    # Prepare prompt for assistant response
    user_prompt = (
        f"The result of your filesystem operation is:\n{fs_output}\n"
        "Please provide a friendly, helpful response to the user."  # noqa: E501
    )
    # Combine conversation history and this prompt
    messages = []
    # Optionally include system instruction
    messages.append({"role": "system", "content": "You are a helpful assistant."})
    # Include past conversation
    messages.extend(state.get("history", []))
    # Add the prompt as a user message
    messages.append({"role": "user", "content": user_prompt})
    # Call LLM to generate assistant reply
    try:
        reply = call_chatgpt(messages)
    except Exception as err:
        reply = f"Error generating response: {err}"
    # Append to history
    state.setdefault("history", []).append({"role": "assistant", "content": reply})
    return state