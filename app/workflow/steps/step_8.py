# app/workflow/steps/step_8.py
from typing import Dict, Any, List

async def execute(workflow_id: str, user_id: str, event: Dict[str, Any], 
                  globals_: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
    """
    Step 8: Conditional Routing
    Route based on agent's action output.
    """
    agent_output = globals_.get("agent_output", {})
    action = agent_output.get("action")
    
    if action == "route_to_refunds":
        logs.append("Step 8: routing to refunds")
        final_status = "routed_to_refunds"
    elif action == "fetch_status":
        logs.append("Step 8: fetching order status")
        final_status = "order_status_returned"
    else:
        logs.append("Step 8: auto-responding")
        final_status = "auto_responded"
    
    return {"success": True, "final_status": final_status}

