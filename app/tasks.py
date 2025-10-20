# app/tasks.py
from celery import Celery
from app.config import settings
import asyncio
import uuid
from app.workflow.workflow_manager import run_workflow_instance

celery = Celery("worker", broker=settings.redis_url, backend=settings.redis_url)
celery.conf.task_acks_late = True
celery.conf.worker_prefetch_multiplier = 1

@celery.task(bind=True, acks_late=True, max_retries=3)
def run_workflow_task(self, customer_id: str, customer_phone_number: str, event: dict):
    workflow_id = str(uuid.uuid4())
    try:
        return asyncio.get_event_loop().run_until_complete(
            run_workflow_instance(workflow_id, customer_id, customer_phone_number, event)
        )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)