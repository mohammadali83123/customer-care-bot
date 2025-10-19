# app/workflow/steps/step_1.py
from typing import Dict, Any, List

async def execute(workflow_id: str, user_id: str, event: Dict[str, Any], 
                  globals_: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
    """
    Step 1: Webhook Trigger
    Log that the webhook has been triggered.
    """
    logs.append("Step 1: webhook triggered")
    return {"success": True}

