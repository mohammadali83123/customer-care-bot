# app/workflow/steps/step_2.py
from typing import Dict, Any, List

async def execute(workflow_id: str, user_id: str, event: Dict[str, Any], 
                  globals_: Dict[str, Any], logs: List[str]) -> Dict[str, Any]:
    """
    Step 2: Initialize Globals
    Set initial user_id and received_event in globals.
    """
    globals_["user_id"] = user_id
    globals_["received_event"] = event
    logs.append("Step 2: initial globals set")
    return {"success": True}

