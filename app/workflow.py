# app/workflow.py
import logging
from typing import Dict, Any
from app.services.apis import call_internal_api_1, call_internal_api_2
from app.services.agent import hardcoded_agentic_response
from app.models import StepResult

logger = logging.getLogger(__name__)

async def run_workflow_instance(workflow_id: str, user_id: str, event: Dict[str, Any]) -> Dict[str, Any]:
    logs = []
    globals_: Dict[str, Any] = {}

    # Step 1 (webhook trigger)
    logs.append("Step 1: webhook triggered")

    # Step 2
    globals_["user_id"] = user_id
    globals_["received_event"] = event
    logs.append("Step 2: initial globals set")

    # Step 3
    payload1 = {"user_id": user_id, "event": event}
    result1: StepResult = await call_internal_api_1(payload1)
    if not result1.success:
        logs.append(f"Step 3 failed: {result1.error}")
        return {"workflow_id": workflow_id, "status": "failed", "reason": "internal_api_1", "logs": logs}
    globals_["api1_response"] = result1.data
    logs.append("Step 3: internal API 1 success")

    # Step 4
    globals_["intermediate_value"] = {"from_api1": result1.data.get("value")} if result1.data else {}
    logs.append("Step 4: set globals after API1")

    # Step 5
    payload2 = {"user_id": user_id, "context": globals_["intermediate_value"]}
    result2: StepResult = await call_internal_api_2(payload2)
    if not result2.success:
        logs.append(f"Step 5 failed: {result2.error}")
        return {"workflow_id": workflow_id, "status": "failed", "reason": "internal_api_2", "logs": logs}
    globals_["api2_response"] = result2.data
    logs.append("Step 5: internal API 2 success")

    # Step 6
    globals_["final_context"] = {
        "api1": globals_.get("api1_response"),
        "api2": globals_.get("api2_response")
    }
    logs.append("Step 6: set final context")

    # Step 7 (hardcoded agent)
    user_msg = event.get("message", "")
    agent_result: StepResult = hardcoded_agentic_response(user_msg, globals_)
    if not agent_result.success:
        logs.append(f"Step 7 failed: {agent_result.error}")
        return {"workflow_id": workflow_id, "status": "failed", "reason": "agent", "logs": logs}
    globals_["agent_output"] = agent_result.data
    logs.append("Step 7: agent executed (hardcoded)")

    # Step 8: condition
    action = agent_result.data.get("action")
    if action == "route_to_refunds":
        logs.append("Step 8: routing to refunds")
        final_status = "routed_to_refunds"
    elif action == "fetch_status":
        logs.append("Step 8: fetching order status")
        final_status = "order_status_returned"
    else:
        logs.append("Step 8: auto-responding")
        final_status = "auto_responded"

    # Step 9
    logs.append("Step 9: terminate")
    return {
        "workflow_id": workflow_id,
        "status": "completed",
        "final_status": final_status,
        "globals": globals_,
        "logs": logs
    }