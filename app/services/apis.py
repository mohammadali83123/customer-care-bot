# app/services/apis.py
import httpx
from app.config import settings
from app.models import StepResult

async def call_internal_api_1(customer_id: str, customer_phone_number: str) -> StepResult:
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(str(settings.internal_api_1), params={"customer_phone_number": customer_phone_number}, timeout=10.0, headers={"Authorization": {settings.access_token}})
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