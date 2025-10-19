# app/workflow/steps/step_6.py
from typing import Dict, Any, List

async def execute(workflow_id: str, user_id: str, event: Dict[str, Any], 
                  globals_: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
    """
    Step 6: Set Final Context
    Combine API responses into final context.
    """
    globals_["final_context"] = {
        "api1": globals_.get("api1_response"),
        "api2": globals_.get("api2_response")
    }
    logs.append("Step 6: set final context")
    return {"success": True}

