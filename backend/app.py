from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, MyAgent is running!"}

@app.post("/chat/send")
async def send_chat(message: dict):
    # TODO: integrate LangGraph workflow to process chat messages
    return {"reply": "This endpoint will process chat messages."}

@app.get("/chat/history")
async def get_history():
    # TODO: return chat history from DB/storage
    return {"history": []}