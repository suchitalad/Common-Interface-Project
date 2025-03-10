from celery import shared_task, current_task, states
from celery.exceptions import Ignore
from celery.utils.log import get_task_logger
from redis import Redis
import traceback
from contextlib import contextmanager
import time
import random

from blocks.celery_tasks import app
from simulationAPI.helpers import ngspice_helper
from simulationAPI.models import Task

logger = get_task_logger(__name__)

        
redis_client = Redis(host='localhost', port=6379, db=0)

LOCK_EXPIRE = 60  # Lock expiry in seconds (fallback for stuck tasks)
MAX_RETRIES = 5  # Maximum retry attempts
BACKOFF_BASE = 2  # Base for exponential backoff

@contextmanager
def session_lock(session_id):
    """ Context manager to ensure a session lock per session_id. """
    lock_key = f"session_lock:{session_id}"
    acquired = redis_client.set(lock_key, 1, ex=LOCK_EXPIRE, nx=True)

    if acquired:
        try:
            yield
        finally:
            redis_client.delete(lock_key)
    else:
        raise Exception(f"Session {session_id} is already running")

@shared_task(bind=True, acks_late=True, max_retries=MAX_RETRIES)
def process_task(self, task_id):
    """ Celery task with session locking and retry logic. """
    try:
        task = Task.objects.get(task_id=task_id)
        session_id = task.session.session_id

        with session_lock(session_id):
            print(f"[{task_id}] Processing session {session_id}")

            # Execute XML processing
            output = ngspice_helper.ExecXml(task)
            state = 'STREAMING' if output == "Streaming" else 'SUCCESS'
            current_process = 'Processed Xml, Streaming Output' if output == "Streaming" else 'Processed Xml, Loading Output'

            self.update_state(state=state, meta={'current_process': current_process})
            print(f"[{task_id}] Finished session {session_id}")
            return output

    except Exception as e:
        print(f"[{task_id}] Skipped session {session_id}: {e}")
        self.update_state(state=states.FAILURE, meta={
            'exc_type': type(e).__name__,
            'exc_message': traceback.format_exc().split('\n')
        })

        if self.request.retries < MAX_RETRIES:
            countdown = BACKOFF_BASE ** self.request.retries + random.uniform(0, 1)
            print(f"[{task_id}] Retrying in {round(countdown, 2)} seconds...")
            raise self.retry(exc=e, countdown=countdown)
        else:
            print(f"[{task_id}] Max retries reached. Task dropped.")
            raise Ignore()