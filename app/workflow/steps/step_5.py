# app/workflow/steps/step_5.py
from typing import Dict, Any, List
from app.services.apis import call_internal_api_2
from app.models import StepResult

async def execute(workflow_id: str, customer_id: str, event: Dict[str, Any], 
                  globals_: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
    """
    Step 5: Call Internal API 2
    Make request to second internal API and store response.
    """
    payload2 = {"customer_id": customer_id, "context": globals_["intermediate_value"]}
    result2: StepResult = await call_internal_api_2(customer_id, payload2)
    
    if not result2.success:
        logs.append(f"Step 5 failed: {result2.error}")
        return {
            "success": False,
            "error": result2.error,
            "reason": "internal_api_2"
        }
    
    globals_["api2_response"] = result2.data
    logs.append("Step 5: internal API 2 success")
    return {"success": True}

