# app/workflow/steps/step_2.py
from typing import Dict, Any, List

async def execute(workflow_id: str, customer_id: str, customer_phone_number: str, event: Dict[str, Any], 
                  globals_: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
    """
    Step 2: Initialize Globals
    Set initial customer_id and received_event in globals.
    """
    globals_["customer_id"] = customer_id
    globals_["customer_phone_number"] = customer_phone_number
    globals_["received_event"] = event
    logs.append("Step 2: initial globals set")
    return {"success": True}

