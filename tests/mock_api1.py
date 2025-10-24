# tests/mock_api1.py
from fastapi import FastAPI

app = FastAPI(title="Mock Internal API 1")

@app.get("/endpoint/{phone_number}")
async def get_customer_registration(phone_number: str):
    print(f"Mock API 1 received GET request for phone: {phone_number}")
    return {
        "value": "mock_value_from_api1",
        "status": "success",
        "phone_number": phone_number,
        "registered": True,
        "customer_id": f"customer_{phone_number}",
        "processed": True
    }

@app.post("/endpoint")
async def api1_endpoint(payload: dict):
    print(f"Mock API 1 received POST: {payload}")
    return {
        "value": "mock_value_from_api1",
        "status": "success",
        "customer_id": payload.get("customer_id"),
        "processed": True
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "mock-api-1"}

