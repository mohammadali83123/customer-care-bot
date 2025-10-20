# app/workflow/workflow_manager.py
import logging
import time
from typing import Dict, Any, Optional
from app.workflow.steps import step_1, step_2, step_3, step_4, step_5, step_6, step_7, step_8, step_9
from app.workflow.visualizer import WorkflowVisualizer

logger = logging.getLogger(__name__)

async def run_workflow_instance(
    workflow_id: str, 
    customer_id: str, 
    customer_phone_number: str, 
    event: Dict[str, Any],
    enable_visualization: bool = True
) -> Dict[str, Any]:
    """
    Main workflow orchestrator that executes all steps in sequence.
    
    Args:
        workflow_id: Unique identifier for this workflow instance
        customer_id: Customer ID for the workflow
        customer_phone_number: Customer phone number for the workflow
        event: Event data to process
        enable_visualization: Whether to generate execution tree visualizations
    """
    logs = []
    globals_: Dict[str, Any] = {}
    final_status = None
    
    # Initialize visualizer
    visualizer = WorkflowVisualizer(workflow_id) if enable_visualization else None
    
    # Define all steps in order
    steps = [
        ("Webhook Triggered", step_1.execute),
        ("Initialize Globals", step_2.execute),
        ("Call Internal API 1", step_3.execute),
        ("Set Globals After API1", step_4.execute),
        ("Call Internal API 2", step_5.execute),
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
                if visualizer:
                    visualizer.add_step(
                        step_name=step_name,
                        step_number=step_num,
                        status="failed",
                        details={"error": result.get("error", "Unknown error")},
                        duration_ms=step_duration
                    )
                    visualizer.mark_complete()
                
                response = {
                    "workflow_id": workflow_id,
                    "status": "failed",
                    "reason": result.get("reason", "unknown"),
                    "logs": logs
                }
                
                if visualizer:
                    response["visualization"] = {
                        "text_tree": visualizer.get_text_tree(),
                        "mermaid": visualizer.get_mermaid_diagram(),
                        "json": visualizer.get_json_tree(),
                        "simple_tree": visualizer.get_simple_tree()
                    }
                
                return response
            
            # Track successful step
            step_details = {}
            if "final_status" in result:
                final_status = result["final_status"]
                step_details["branch"] = final_status
            
            if visualizer:
                visualizer.add_step(
                    step_name=step_name,
                    step_number=step_num,
                    status="completed",
                    details=step_details,
                    duration_ms=step_duration
                )
                
        except Exception as e:
            step_duration = (time.time() - step_start_time) * 1000
            logger.error(f"Error in {step_name}: {str(e)}")
            logs.append(f"{step_name} error: {str(e)}")
            
            if visualizer:
                visualizer.add_step(
                    step_name=step_name,
                    step_number=step_num,
                    status="failed",
                    details={"exception": str(e)},
                    duration_ms=step_duration
                )
                visualizer.mark_complete()
            
            response = {
                "workflow_id": workflow_id,
                "status": "failed",
                "reason": "exception",
                "error": str(e),
                "logs": logs
            }
            
            if visualizer:
                response["visualization"] = {
                    "text_tree": visualizer.get_text_tree(),
                    "mermaid": visualizer.get_mermaid_diagram(),
                    "json": visualizer.get_json_tree(),
                    "simple_tree": visualizer.get_simple_tree()
                }
            
            return response
    
    # Mark workflow complete
    if visualizer:
        visualizer.mark_complete()
    
    # Return successful completion
    response = {
        "workflow_id": workflow_id,
        "status": "completed",
        "final_status": final_status,
        "globals": globals_,
        "logs": logs
    }
    
    # Add visualization data
    if visualizer:
        response["visualization"] = {
            "text_tree": visualizer.get_text_tree(),
            "mermaid": visualizer.get_mermaid_diagram(),
            "json": visualizer.get_json_tree(),
            "simple_tree": visualizer.get_simple_tree()
        }
    
    return response

