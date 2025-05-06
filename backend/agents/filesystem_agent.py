import os
from pathlib import Path

def read_file(path: str) -> str:
    """Read and return the contents of a file."""
    return Path(path).read_text()

def write_file(path: str, content: str) -> None:
    """Write content to a file, creating it if necessary."""
    # Ensure parent directory exists before writing
    file_path = Path(path)
    parent = file_path.parent
    if parent and not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)

def delete_file(path: str) -> None:
    """Delete a file if it exists."""
    try:
        Path(path).unlink()
    except FileNotFoundError:
        pass

def move_file(src: str, dest: str) -> None:
    """Move or rename a file."""
    Path(src).rename(dest)