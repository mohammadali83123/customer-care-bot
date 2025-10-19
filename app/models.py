# app/models.py
from pydantic import BaseModel
from typing import Dict, Any, Optional

class WebhookRequest(BaseModel):
    user_id: str
    event: Dict[str, Any]

class StepResult(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None