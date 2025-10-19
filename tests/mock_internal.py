# mock_internal.py
from fastapi import FastAPI
app = FastAPI()

@app.post("/api1")
async def api1(payload: dict):
    return {"value": "v1", "raw": payload}

@app.post("/api2")
async def api2(payload: dict):
    return {"result": "ok", "received": payload}