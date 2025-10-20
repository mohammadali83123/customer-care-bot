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
        run_workflow_task.delay(payload.customer_id, payload.customer_phone_number, payload.event)
        return {"status": "accepted", "message": "workflow queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflow/run")
async def run_workflow_sync(payload: WebhookRequest):
    """
    Run workflow synchronously and return full result with visualization.
    Useful for testing and debugging.
    """
    try:
        workflow_id = str(uuid.uuid4())
        result = await run_workflow_instance(
            workflow_id=workflow_id,
            customer_id=payload.customer_id,
            customer_phone_number=payload.customer_phone_number,
            event=payload.event,
            enable_visualization=True
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflow/visualize", response_class=PlainTextResponse)
async def visualize_workflow(payload: WebhookRequest):
    """
    Run workflow and return ASCII tree visualization.
    """
    try:
        workflow_id = str(uuid.uuid4())
        result = await run_workflow_instance(
            workflow_id=workflow_id,
            customer_id=payload.customer_id,
            customer_phone_number=payload.customer_phone_number,
            event=payload.event,
            enable_visualization=True
        )
        
        if "visualization" in result:
            return result["visualization"]["text_tree"]
        else:
            return "Visualization not available"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflow/diagram", response_class=PlainTextResponse)
async def get_workflow_diagram(payload: WebhookRequest):
    """
    Run workflow and return Mermaid diagram syntax.
    Copy this to https://mermaid.live to visualize.
    """
    try:
        workflow_id = str(uuid.uuid4())
        result = await run_workflow_instance(
            workflow_id=workflow_id,
            customer_id=payload.customer_id,
            customer_phone_number=payload.customer_phone_number,
            event=payload.event,
            enable_visualization=True
        )
        
        if "visualization" in result:
            return result["visualization"]["mermaid"]
        else:
            return "Diagram not available"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """API information."""
    return {
        "service": "Customer Care Bot",
        "endpoints": {
            "POST /webhook": "Queue workflow asynchronously",
            "POST /workflow/run": "Run workflow synchronously with full visualization",
            "POST /workflow/visualize": "Get ASCII tree visualization",
            "POST /workflow/diagram": "Get Mermaid diagram (paste at mermaid.live)"
        }
    }