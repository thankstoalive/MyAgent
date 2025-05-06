from typing import Any
from backend.models.chat_state import ChatState
from backend.agents.filesystem_agent import (
    read_file,
    write_file,
    delete_file,
    move_file,
)

def execute_fs_node(state: ChatState) -> ChatState:
    """
    Execute the filesystem command stored in state['last_command'].
    Stores the result or error message in state['fs_result'].
    """
    cmd = state.get("last_command", "").strip()
    output = ""
    if not cmd or cmd.lower() == "none":
        output = "No filesystem operation requested."
    else:
        parts = cmd.split(":")
        op = parts[0].lower()
        try:
            if op == "read" and len(parts) >= 2:
                content = read_file(parts[1])
                output = f"Read file '{parts[1]}':\n{content}"
            elif op == "write" and len(parts) >= 3:
                path, data = parts[1], parts[2]
                write_file(path, data)
                output = f"Wrote to file '{path}'."
            elif op == "delete" and len(parts) >= 2:
                delete_file(parts[1])
                output = f"Deleted file '{parts[1]}'."
            elif op == "move" and len(parts) >= 3:
                src, dst = parts[1], parts[2]
                move_file(src, dst)
                output = f"Moved file from '{src}' to '{dst}'."
            else:
                output = f"Unrecognized or malformed command: '{cmd}'"
        except Exception as err:
            output = f"Error executing '{cmd}': {err}"
    state["fs_result"] = output
    return state