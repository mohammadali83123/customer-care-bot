# app/workflow/workflow_manager.py
import logging
from typing import Dict, Any
from app.workflow.steps import step_1, step_2, step_3, step_4, step_5, step_6, step_7, step_8, step_9

logger = logging.getLogger(__name__)

async def run_workflow_instance(workflow_id: str, user_id: str, event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main workflow orchestrator that executes all steps in sequence.
    """
    logs = []
    globals_: Dict[str, Any] = {}
    final_status = None
    
    # Define all steps in order
    steps = [
        ("Step 1", step_1.execute),
        ("Step 2", step_2.execute),
        ("Step 3", step_3.execute),
        ("Step 4", step_4.execute),
        ("Step 5", step_5.execute),
        ("Step 6", step_6.execute),
        ("Step 7", step_7.execute),
        ("Step 8", step_8.execute),
        ("Step 9", step_9.execute),
    ]
    
    # Execute steps sequentially
    for step_name, step_func in steps:
        try:
            result = await step_func(workflow_id, user_id, event, globals_, logs)
            
            # Check if step failed
            if not result.get("success"):
                return {
                    "workflow_id": workflow_id,
                    "status": "failed",
                    "reason": result.get("reason", "unknown"),
                    "logs": logs
                }
            
            # Capture final_status from step 8
            if "final_status" in result:
                final_status = result["final_status"]
                
        except Exception as e:
            logger.error(f"Error in {step_name}: {str(e)}")
            logs.append(f"{step_name} error: {str(e)}")
            return {
                "workflow_id": workflow_id,
                "status": "failed",
                "reason": "exception",
                "error": str(e),
                "logs": logs
            }
    
    # Return successful completion
    return {
        "workflow_id": workflow_id,
        "status": "completed",
        "final_status": final_status,
        "globals": globals_,
        "logs": logs
    }

