import os
import time
import asyncio
from openai import OpenAI
# from services.summary_services import summarize

from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
api_key = os.environ.get("OPENAI_API_KEY")

# @celery.task(name="create_task")
# def create_task(task_type):
#     time.sleep(int(task_type) * 10)
#     return True

# @celery.task(name="summarize_task")
# def summarize_task(model, document):
#     loop = asyncio.get_event_loop()
#     result = loop.run_until_complete(summarize(api_key, model, document))
#     return result