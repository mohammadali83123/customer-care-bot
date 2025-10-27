# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from app.models import WebhookRequest
from app.tasks import run_workflow_task
from app.workflow.workflow_manager import run_workflow_instance
import uuid

app = FastAPI(title="Customer Care Bot")

@app.post("/webhook")
async def webhook(payload: WebhookRequest):
    """Queue workflow execution asynchronously via Celery."""
    try:
        # .delay() is a Celery method to queue the task asynchronously for execution by a worker
        run_workflow_task.delay(payload.customer_id, payload.customer_phone_number, payload.event)
        return {"status": "accepted", "message": "workflow queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """API information."""
    return {
        "service": "Customer Care Bot",
        "endpoints": {
            "POST /webhook": "Queue workflow asynchronously",
        }
    }