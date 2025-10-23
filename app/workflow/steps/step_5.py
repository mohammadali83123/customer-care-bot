# app/workflow/steps/step_5.py
from typing import Dict, Any, List
from app.services.apis import fetch_customer_orders_api
from app.models import StepResult

async def execute(workflow_id: str, customer_id: str, customer_phone_number: str, event: Dict[str, Any], 
                  globals_: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
    """
    Step 5: Call FETCH_CUSTOMER_ORDERS_API
    Make request to second internal API and store response.
    """
    payload2 = {"store_number": customer_phone_number}
    result2: StepResult = await fetch_customer_orders_api(payload2)
    
    if not result2.success:
        logs.append(f"Step 5 failed: {result2.error}")
        return {
            "success": False,
            "error": result2.error,
            "reason": "FETCH_CUSTOMER_ORDERS_API_FAILED"
        }
    
    globals_["api2_response"] = result2.data
    logs.append("Step 5: FETCH_CUSTOMER_ORDERS_API_SUCCESS")
    return {"success": True}

