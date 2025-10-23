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

@app.post("/workflow/beautified", response_class=PlainTextResponse)
async def get_beautified_workflow(payload: WebhookRequest):
    """
    Run workflow and return beautified output with colors and emojis.
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
        
        if "beautified_output" in result:
            return result["beautified_output"]["tree"]
        else:
            return "Beautified output not available"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflow/logs", response_class=PlainTextResponse)
async def get_complete_logs(payload: WebhookRequest):
    """
    Run workflow and return complete beautified logs with all API responses.
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
        
        if "beautified_output" in result:
            return result["beautified_output"]["logs"]
        else:
            return "Beautified logs not available"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflow/complete", response_class=PlainTextResponse)
async def get_complete_output(payload: WebhookRequest):
    """
    Run workflow and return complete beautified output (tree + logs).
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
        
        if "beautified_output" in result:
            tree = result["beautified_output"]["tree"]
            logs = result["beautified_output"]["logs"]
            return f"{tree}\n\n{logs}"
        else:
            return "Beautified output not available"
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
            "POST /workflow/diagram": "Get Mermaid diagram (paste at mermaid.live)",
            "POST /workflow/beautified": "Get beautified tree output with colors and emojis",
            "POST /workflow/logs": "Get complete beautified logs with all API responses",
            "POST /workflow/complete": "Get complete beautified output (tree + logs)"
        }
    }