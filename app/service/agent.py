# app/services/agent.py
from typing import Dict, Any
from app.entity.models import StepResult

def hardcoded_agentic_response(customer_message: str, globals_: Dict[str, Any]) -> StepResult:
    """
    Simulated agentic response for Step 7 (hardcoded).
    Returns a simple dict used by Step 8 condition handling.
    """
    msg = (customer_message or "").lower()
    if "refund" in msg or "return" in msg:
        body = {"intent": "refund_request", "confidence": 0.98, "action": "route_to_refunds"}
    elif "status" in msg or "where is my order" in msg:
        body = {"intent": "order_status", "confidence": 0.95, "action": "fetch_status"}
    else:
        body = {"intent": "general_query", "confidence": 0.6, "action": "respond_with_info"}
    return StepResult(success=True, data=body)