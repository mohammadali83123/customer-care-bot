# app/services/apis.py
import httpx
from app.config import settings
from app.models import StepResult

async def check_customer_registration_api(customer_phone_number: str) -> StepResult:
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(str(settings.CHECK_CUSTOMER_REGISTRATION_API_URL), params={"customer_phone_number": customer_phone_number}, timeout=10.0, headers={"Authorization": {settings.ACCESS_TOKEN}})
            resp.raise_for_status()
            return StepResult(success=True, data=resp.json())
        except Exception as e:
            return StepResult(success=False, error=str(e))

async def call_internal_api_2(payload: dict) -> StepResult:
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(str(settings.FETCH_CUSTOMER_ORDERS_API_URL), json=payload, timeout=10.0)
            resp.raise_for_status()
            return StepResult(success=True, data=resp.json())
        except Exception as e:
            return StepResult(success=False, error=str(e))