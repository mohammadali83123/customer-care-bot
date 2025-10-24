# tests/mock_api2.py
from fastapi import FastAPI

app = FastAPI(title="Mock Internal API 2")

@app.post("/endpoint")
async def api2_endpoint(payload: dict):
    print(f"Mock API 2 received: {payload}")
    return {
        "result": "processed_by_api2",
        "status": "success",
        "orders": [
            {
                "order_id": "order_123",
                "status": "shipped",
                "items": ["item1", "item2"],
                "total": 100.50
            }
        ],
        "context": payload.get("context"),
        "recommendation": "continue_workflow"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "mock-api-2"}

