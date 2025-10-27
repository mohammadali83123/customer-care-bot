# app/workflow/workflow_manager.py
import logging
import time
from typing import Dict, Any
from app.service.workflow.steps import step_1, step_2, step_3, step_4, step_5, step_6, step_7, step_8, step_9

logger = logging.getLogger(__name__)

async def run_workflow_instance(
    workflow_id: str, 
    customer_id: str, 
    customer_phone_number: str, 
    event: Dict[str, Any]
) -> Dict[str, Any]:

    """
    Main workflow orchestrator that executes all steps in sequence.
    
    Args:
        workflow_id: Unique identifier for this workflow instance
        customer_id: Customer ID for the workflow
        customer_phone_number: Customer phone number for the workflow
        event: Event data to process
    """
    logs = []
    globals_: Dict[str, Any] = {}
    final_status = None
    
    # Define all steps in order
    steps = [
        ("Webhook Triggered", step_1.execute),
        ("Initialize Globals", step_2.execute),
        ("Call CHECK_CUSTOMER_REGISTRATION_API", step_3.execute),
        ("Set Globals After API1", step_4.execute),
        ("Call FETCH_CUSTOMER_ORDERS_API", step_5.execute),
        ("Set Final Context", step_6.execute),
        ("Run Agent", step_7.execute),
        ("Conditional Routing", step_8.execute),
        ("Terminate", step_9.execute),
    ]
    
    # Execute steps sequentially
    for step_num, (step_name, step_func) in enumerate(steps, start=1):
        step_start_time = time.time()
        
        try:
            result = await step_func(workflow_id, customer_id, customer_phone_number, event, globals_, logs)
            step_duration = (time.time() - step_start_time) * 1000  # Convert to ms
            
            # Check if step failed
            if not result.get("success"):
                response = {
                    "workflow_id": workflow_id,
                    "status": "failed",
                    "reason": result.get("reason", "unknown"),
                    "logs": logs
                }
                
                return response
            
            # Track successful step
            step_details = {}
            if "final_status" in result:
                final_status = result["final_status"]
                step_details["branch"] = final_status
            
                
        except Exception as e:
            step_duration = (time.time() - step_start_time) * 1000
            logger.error(f"Error in {step_name}: {str(e)}")
            logs.append(f"{step_name} error: {str(e)}")
            
            
            response = {
                "workflow_id": workflow_id,
                "status": "failed",
                "reason": "exception",
                "error": str(e),
                "logs": logs
            }
            
            return response
    
    # Return successful completion
    response = {
        "workflow_id": workflow_id,
        "status": "completed",
        "final_status": final_status,
        "globals": globals_,
        "logs": logs
    }
    
    return response

