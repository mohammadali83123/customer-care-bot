# app/services/apis.py
import httpx
from app.config import settings
from app.models import StepResult

async def call_internal_api_1(payload: dict) -> StepResult:
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(str(settings.internal_api_1), json=payload, timeout=10.0)
            resp.raise_for_status()
            return StepResult(success=True, data=resp.json())
        except Exception as e:
            return StepResult(success=False, error=str(e))

async def call_internal_api_2(payload: dict) -> StepResult:
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(str(settings.internal_api_2), json=payload, timeout=10.0)
            resp.raise_for_status()
            return StepResult(success=True, data=resp.json())
        except Exception as e:
            return StepResult(success=False, error=str(e))