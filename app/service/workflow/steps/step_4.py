# app/workflow/steps/step_4.py
from typing import Dict, Any, List

async def execute(workflow_id: str, customer_id: str, customer_phone_number: str,event: Dict[str, Any], 
                  globals_: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
    """
    Step 4: Set Globals After API1
    Transform and store intermediate values from API1 response.
    """
    customer_registration_response = globals_.get("customer_registration_response")
    globals_["intermediate_value"] = {
        "from_customer_registration": customer_registration_response.get("value") if customer_registration_response else None
    }
    logs.append("Step 4: set globals after API1")
    return {"success": True}

