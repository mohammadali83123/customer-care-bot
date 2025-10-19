# tests/mock_api1.py
from fastapi import FastAPI

app = FastAPI(title="Mock Internal API 1")

@app.post("/endpoint")
async def api1_endpoint(payload: dict):
    print(f"Mock API 1 received: {payload}")
    return {
        "value": "mock_value_from_api1",
        "status": "success",
        "user_id": payload.get("user_id"),
        "processed": True
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "mock-api-1"}

