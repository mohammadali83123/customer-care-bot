# app/tasks.py
from celery import Celery
from app.config import settings
import asyncio
import uuid
import logging
from app.workflow.workflow_manager import run_workflow_instance

# Set up logging for Celery
logger = logging.getLogger(__name__)

celery = Celery("worker", broker=settings.REDIS_URL, backend=settings.REDIS_URL)
celery.conf.task_acks_late = True
celery.conf.worker_prefetch_multiplier = 1

@celery.task(bind=True, acks_late=True, max_retries=3)
def run_workflow_task(self, customer_id: str, customer_phone_number: str, event: dict):
    workflow_id = str(uuid.uuid4())
    try:
        # Run the workflow
        result = asyncio.get_event_loop().run_until_complete(
            run_workflow_instance(workflow_id, customer_id, customer_phone_number, event)
        )
        
        return result
        
    except Exception as exc:
        print(f"\n❌ WORKFLOW EXECUTION FAILED: {str(exc)}")
        print("="*80 + "\n")
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)