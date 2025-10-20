# app/workflow/steps/step_7.py
from typing import Dict, Any, List
from app.services.agent import hardcoded_agentic_response
from app.models import StepResult

async def execute(workflow_id: str, customer_id: str, event: Dict[str, Any], 
                  globals_: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
    """
    Step 7: Run Agent
    Execute the hardcoded agentic response logic.
    """
    customer_msg = event.get("message", "")
    agent_result: StepResult = hardcoded_agentic_response(customer_msg, globals_)
    
    if not agent_result.success:
        logs.append(f"Step 7 failed: {agent_result.error}")
        return {
            "success": False,
            "error": agent_result.error,
            "reason": "agent"
        }
    
    globals_["agent_output"] = agent_result.data
    logs.append("Step 7: agent executed (hardcoded)")
    return {"success": True}

