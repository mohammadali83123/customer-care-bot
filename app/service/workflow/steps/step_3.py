# app/workflow/steps/step_3.py
from typing import Dict, Any, List
from app.service.apis import check_customer_registration_api
from app.entity.models import StepResult

async def execute(workflow_id: str, customer_id: str, customer_phone_number: str, event: Dict[str, Any], 
                  globals_: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
    """
    Step 3: Call Check customer registration API
    Make request to first internal API and store response.
    """
    normalized_customer_phone_number = customer_phone_number.replace('+92', '0')
    result1: StepResult = await check_customer_registration_api(normalized_customer_phone_number)
    
    if not result1.success:
        logs.append(f"Step 3 failed: {result1.error}")
        return {
            "success": False,
            "error": result1.error,
            "reason": "CHECK_CUSTOMER_REGISTRATION_API_FAILED"
        }
    
    globals_["customer_registration_response"] = result1.data

    return {"success": True}

