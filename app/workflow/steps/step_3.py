# app/workflow/steps/step_3.py
from typing import Dict, Any, List
from app.services.apis import call_internal_api_1
from app.models import StepResult

async def execute(workflow_id: str, user_id: str, event: Dict[str, Any], 
                  globals_: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
    """
    Step 3: Call Internal API 1
    Make request to first internal API and store response.
    """
    payload1 = {"user_id": user_id, "event": event}
    result1: StepResult = await call_internal_api_1(payload1)
    
    if not result1.success:
        logs.append(f"Step 3 failed: {result1.error}")
        return {
            "success": False,
            "error": result1.error,
            "reason": "internal_api_1"
        }
    
    globals_["api1_response"] = result1.data
    logs.append("Step 3: internal API 1 success")
    return {"success": True}

