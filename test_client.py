#!/usr/bin/env python3
"""
Python script to test the MyAgent FastAPI endpoints.
Requires `requests` (pip install requests).
Run with: python test_client.py
"""
import os
import requests

BASE_URL = os.getenv("MYAGENT_BASE", "http://127.0.0.1:8000")

def send(msg: str) -> str:
    """Send a chat message and return the assistant's reply."""
    resp = requests.post(
        f"{BASE_URL}/chat/send",
        json={"content": msg},
        headers={"Content-Type": "application/json"},
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("reply", "")

def history() -> list:
    """Fetch the full chat history."""
    resp = requests.get(f"{BASE_URL}/chat/history")
    resp.raise_for_status()
    return resp.json().get("history", [])

def main():
    print("1) List files:", send("파일 목록 보여줘"))
    # Ensure test_dir exists for write
    if not os.path.isdir("test_dir"):
        os.makedirs("test_dir", exist_ok=True)
    print("2) Create file:", send("test_dir/test.txt 파일 생성해줘"))
    print("3) Read file:", send("test_dir/test.txt 내용 보여줘"))
    print("4) Move file:", send("test_dir/test.txt를 test_dir/renamed.txt로 이동해줘"))
    print("5) Delete file:", send("test_dir/renamed.txt 삭제해줘"))
    print("Full history:", history())

if __name__ == "__main__":
    main()