#!/usr/bin/env python3
"""
Demo script to showcase workflow visualization features.
"""
import asyncio
import sys
sys.path.insert(0, '/customers/Ali/Documents/customer-care-bot')

from app.workflow.workflow_manager import run_workflow_instance
from app.models import StepResult
import uuid

# Mock the API calls for demo purposes
async def mock_api1(payload):
    return StepResult(success=True, data={"value": "mock_value_from_api1"})

async def mock_api2(payload):
    return StepResult(success=True, data={"result": "processed_by_api2"})

async def demo_visualization():
    """Run workflow with different scenarios and show visualizations."""
    
    # Monkey-patch the API calls
    import app.workflow.steps.step_3 as step3
    import app.workflow.steps.step_5 as step5
    step3.call_internal_api_1 = mock_api1
    step5.call_internal_api_2 = mock_api2
    
    print("=" * 80)
    print("WORKFLOW VISUALIZATION DEMO")
    print("=" * 80)
    print()
    
    # Scenario 1: Order Status Query
    print("\n" + "=" * 80)
    print("SCENARIO 1: Order Status Query")
    print("=" * 80)
    
    result1 = await run_workflow_instance(
        workflow_id=str(uuid.uuid4()),
        customer_id="demo-customer-1",
        event={"message": "where is my order?"},
        enable_visualization=True
    )
    
    print("\n📊 TEXT TREE VISUALIZATION:")
    print(result1["visualization"]["text_tree"])
    
    print("\n\n📈 SIMPLE TREE:")
    print(result1["visualization"]["simple_tree"])
    
    print(f"\n\n✅ Final Status: {result1['final_status']}")
    print(f"Status: {result1['status']}")
    
    # Scenario 2: Refund Request
    print("\n\n" + "=" * 80)
    print("SCENARIO 2: Refund Request")
    print("=" * 80)
    
    result2 = await run_workflow_instance(
        workflow_id=str(uuid.uuid4()),
        customer_id="demo-customer-2",
        event={"message": "I want a refund"},
        enable_visualization=True
    )
    
    print("\n📊 TEXT TREE VISUALIZATION:")
    print(result2["visualization"]["text_tree"])
    
    print(f"\n\n✅ Final Status: {result2['final_status']}")
    
    # Scenario 3: General Query
    print("\n\n" + "=" * 80)
    print("SCENARIO 3: General Query")
    print("=" * 80)
    
    result3 = await run_workflow_instance(
        workflow_id=str(uuid.uuid4()),
        customer_id="demo-customer-3",
        event={"message": "Hi, how are you?"},
        enable_visualization=True
    )
    
    print("\n📊 TEXT TREE VISUALIZATION:")
    print(result3["visualization"]["text_tree"])
    
    print(f"\n\n✅ Final Status: {result3['final_status']}")
    
    # Show Mermaid Diagram
    print("\n\n" + "=" * 80)
    print("MERMAID DIAGRAM (Copy to https://mermaid.live)")
    print("=" * 80)
    print()
    print(result1["visualization"]["mermaid"])
    
    print("\n\n" + "=" * 80)
    print("JSON EXPORT EXAMPLE")
    print("=" * 80)
    import json
    viz_data = json.loads(result1["visualization"]["json"])
    print(json.dumps(viz_data, indent=2))
    
    print("\n\n" + "=" * 80)
    print("DEMO COMPLETE!")
    print("=" * 80)
    print("\nKey Features:")
    print("  ✓ Real-time execution tracking")
    print("  ✓ Step-by-step timing information")
    print("  ✓ Branch visualization (conditional routing)")
    print("  ✓ Multiple export formats (ASCII, Mermaid, JSON)")
    print("  ✓ Success/failure status indicators")
    print()

if __name__ == "__main__":
    asyncio.run(demo_visualization())

