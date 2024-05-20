from celery.result import AsyncResult
from fastapi import Body, FastAPI, Form, Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
import os
from worker import create_task, summarize_task

router = APIRouter()

@router.post("/tasks", status_code=201, tags=["General Tasks"], description="Run a generic task.")
def run_task(payload = Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@router.get("/tasks/{task_id}", tags=["General Tasks"], description="Get the status of a task by its ID.")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)


