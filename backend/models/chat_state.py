from typing import TypedDict, List, Dict

class ChatState(TypedDict):
    """
    Represents the chat session state, including message history and the last parsed filesystem command.
    """
    history: List[Dict[str, str]]  # [{"role": "user"|"assistant", "content": ...}, ...]
    last_command: str               # e.g., "read:/path/to/file"