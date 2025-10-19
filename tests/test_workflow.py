# tests/test_workflow.py
import pytest
from app.workflow import run_workflow_instance
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

    monkeypatch.setattr("app.services.apis.call_internal_api_1", fake_api1)
    monkeypatch.setattr("app.services.apis.call_internal_api_2", fake_api2)

    result = await run_workflow_instance("wf-1", "user-1", {"message":"what's my order status?"})
    assert result["status"] == "completed"
    assert result["final_status"] in ("order_status_returned", "auto_responded", "routed_to_refunds")