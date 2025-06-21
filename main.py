from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
from mem0 import AsyncMemoryClient
from datetime import datetime

app = FastAPI()
mem0 = AsyncMemoryClient(api_key=os.getenv("MEM0_API_KEY"))
DEFAULT_USER_ID = os.getenv("MEM0_DEFAULT_USER_ID", "demo_user_001")

@app.get("/getDate")
async def get_date(_: Request):
    now = datetime.utcnow()
    date_str = now.strftime("%B %d, %Y")
    weekday = now.strftime("%A")
    print(f"[📅 /getDate] → {weekday}, {date_str}")
    return {
        "date": date_str,
        "weekday": weekday
    }

class AddMemoriesPayload(BaseModel):
    message: str

class RetrieveMemoriesPayload(BaseModel):
    query: str

@app.post("/addMemories")
async def add_memories(payload: AddMemoriesPayload):
    await mem0.add(
        messages=[{"role": "user", "content": payload.message}],
        user_id=DEFAULT_USER_ID,
        version="v2"
    )
    print(f"[🧠 /addMemories] {payload.message}")
    return {"status": "stored"}

@app.post("/retrieveMemories")
async def retrieve_memories(payload: RetrieveMemoriesPayload):
    response = await mem0.search(
        query=payload.query,
        user_id=DEFAULT_USER_ID,
        filters={"user_id": DEFAULT_USER_ID},
        version="v2"
    )
    memory = response[0]["memory"] if response else ""
    print(f"[🔍 retrieveMemories] {memory}")
    return {"memory": memory or "none"}