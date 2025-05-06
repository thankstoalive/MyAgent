from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, MyAgent is running!"}

from backend.models.chat_state import ChatState
from backend.agents.chat_graph import build_chat_graph

# Initialize in-memory chat state and graph
_chat_state: ChatState = ChatState(history=[], last_command="")
_chat_graph = build_chat_graph()

@app.post("/chat/send")
async def send_chat(request: dict):
    """
    Receive a user message, run through the chat graph, and return the assistant reply.
    Expects JSON: {"content": "user message text"}
    """
    # Extract user message text
    user_text = request.get("content") or request.get("message") or ""
    # Append user message to history
    _chat_state["history"].append({"role": "user", "content": user_text})
    # Run the LangGraph workflow to update state and generate assistant response
    try:
        result = _chat_graph.invoke(_chat_state)
        # _chat_graph.invoke mutates _chat_state in place and returns it
        reply = _chat_state.get("history", [])[-1].get("content", "")
    except Exception as err:
        # On error, return a fallback message
        reply = f"Error processing request: {err}"
    return {"reply": reply}

@app.get("/chat/history")
async def get_history():
    """
    Return the full chat history.
    """
    return {"history": _chat_state.get("history", [])}