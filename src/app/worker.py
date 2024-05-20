import asyncio, os, time, uuid
from services.v1.summary_services import summarize, create_summarization
from datetime import datetime
from models.models import Summary
from database.database import database

from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
api_key = os.environ.get("OPENAI_API_KEY")

@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

@celery.task(name="summarize_task")
def summarize_task(model, document):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(summarize(api_key, model, document))
    return result

@celery.task(name="create_summary_task")
def create_summary_task(model, document, doc_id):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(create_summarization_and_store(api_key, model, document, doc_id))
    return result


async def create_summarization_and_store(api_key, model, document, doc_id):
    result = await create_summarization(api_key, model, document)
    
    new_summary = {
        "id": str(uuid.uuid4()),
        "doc_id": doc_id,
        "model": model,
        "content": result,
        "updatedAt": datetime.utcnow().isoformat(),
        "createdAt": datetime.utcnow().isoformat()
    }

    query = Summary.__table__.insert().values(new_summary)
    await database.execute(query)
    
    return new_summary
