# tests/test_workflow.py
import pytest
from app.workflow.workflow_manager import run_workflow_instance
import asyncio
from app.models import StepResult

class Dummy(StepResult):
    pass

@pytest.mark.asyncio
async def test_workflow_happy_path(monkeypatch):
    async def fake_api1(payload):
        return StepResult(success=True, data={"value":"v1"})
    async def fake_api2(payload):
        return StepResult(success=True, data={"result":"ok"})

    monkeypatch.setattr("app.workflow.steps.step_3.check_customer_registration_api", fake_api1)
    monkeypatch.setattr("app.workflow.steps.step_5.fetch_customer_orders_api", fake_api2)

    result = await run_workflow_instance("wf-1", "customer-1", "+923001234567", {"message":"what's my order status?"})
    assert result["status"] == "completed"
    assert result["final_status"] in ("order_status_returned", "auto_responded", "routed_to_refunds")