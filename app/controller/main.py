# app/main.py
from fastapi import FastAPI, HTTPException
from app.entity.models import WebhookRequest
from app.celery_config.tasks import run_workflow_task
import uuid

app = FastAPI(title="Customer Care Bot")

@app.post("/webhook")
async def webhook(payload: WebhookRequest):
    """Queue workflow execution asynchronously via Celery."""
    try:
        workflow_id = str(uuid.uuid4())
        # .delay() is a Celery method to queue the task asynchronously for execution by a worker
        run_workflow_task.delay(workflow_id, payload.customer_id, payload.customer_phone_number, payload.event)
        return {"status": "accepted", "message": "workflow queued", "workflow_id": workflow_id}
    
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