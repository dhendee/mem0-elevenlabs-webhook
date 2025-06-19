from fastapi import FastAPI
from pydantic import BaseModel
import os
from mem0 import AsyncMemoryClient

app = FastAPI()
mem0 = AsyncMemoryClient(api_key=os.getenv("MEM0_API_KEY"))
DEFAULT_USER_ID = os.getenv("MEM0_DEFAULT_USER_ID", "demo_user_001")

class AddMemoriesPayload(BaseModel):
    message: str

class RetrieveMemoriesPayload(BaseModel):
    query: str

@app.post("/addMemories")
async def add_memories(payload: AddMemoriesPayload):
    print(f"[🧠 /addMemories] {payload.message}")
    await mem0.add(
        messages=[{"role": "user", "content": payload.message}],
        user_id=DEFAULT_USER_ID,
        version="v2"
    )
    return {"status": "stored"}

@app.post("/retrieveMemories")
async def retrieve_memories(payload: RetrieveMemoriesPayload):
    print(f"[🔍 /retrieveMemories] {payload.query}")
    response = await mem0.search(
        query=payload.query,
        user_id=DEFAULT_USER_ID,
        filters={"user_id": DEFAULT_USER_ID},
        version="v2"
    )
    memory = response[0]["memory"] if results else ""
    return {"memory": memory or "none"}