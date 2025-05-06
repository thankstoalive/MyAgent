import os
from typing import Any, Dict
from backend.models.chat_state import ChatState
from backend.agents.llm_client import call_chatgpt

def intent_parsing_node(state: ChatState) -> ChatState:
    """
    Parse the latest user message to determine if a filesystem operation is requested.
    Updates state['last_command'] with a command string or 'none'.
    """
    # Extract latest user message
    if not state.get("history"):
        state["last_command"] = "none"
        return state
    last_msg = state["history"][-1]
    user_text = last_msg.get("content", "")

    # Prepare LLM prompt to parse intent
    system_prompt = (
        "You are a parser that extracts filesystem commands from user requests. "
        "Respond with a single command in one of these formats:\n"
        "list:/path/to/directory\n"
        "read:/path/to/file\n"
        "write:/path/to/file:content_to_write\n"
        "delete:/path/to/file\n"
        "move:/src/path:/dst/path\n"
        "If the request is not a filesystem operation, respond with 'none'. "
        "If the user requests a listing without specifying a path, assume the current directory '.' and return 'list:.'"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_text},
    ]
    # Call LLM to parse intent
    try:
        cmd = call_chatgpt(messages).strip()
    except Exception:
        cmd = "none"
    # Fallback: if parsing yields none, but user requests listing, default to current dir
    if cmd.lower() == "none":
        text = user_text.lower()
        if "파일 목록" in text or "list files" in text or text.startswith("list"):
            cmd = f"list:."
    state["last_command"] = cmd
    return state