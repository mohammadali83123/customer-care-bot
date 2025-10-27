# app/workflow/steps/step_6.py
from typing import Dict, Any, List

async def execute(workflow_id: str, customer_id: str, customer_phone_number: str, event: Dict[str, Any], 
                  globals_: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
    """
    Step 6: Set Final Context
    Combine API responses into final context.
    """
    globals_["final_context"] = {
        "customer_registration_response": globals_.get("customer_registration_response"),
        "customer_orders_response": globals_.get("customer_orders_response")
    }
    logs.append("Step 6: set final context")
    return {"success": True}

