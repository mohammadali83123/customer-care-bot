# app/main.py
from fastapi import FastAPI, HTTPException
from app.models import WebhookRequest
from app.tasks import run_workflow_task

app = FastAPI(title="Customer Care Bot")

@app.post("/webhook")
async def webhook(payload: WebhookRequest):
    try:
        run_workflow_task.delay(payload.user_id, payload.event)
        return {"status": "accepted", "message": "workflow queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))