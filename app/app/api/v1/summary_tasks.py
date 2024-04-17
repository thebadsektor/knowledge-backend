import uuid
import random
from typing import List

from fastapi import APIRouter, HTTPException, WebSocket
from openai import OpenAI

from app.models.models import SummaryTask
from app.schemas.schemas import SummaryTaskSchema
from app.database.database import database

router = APIRouter()

async def create_summary_tasks():
    async with database.transaction():
        await database.execute("DROP TABLE IF EXISTS summary_tasks")
        await database.execute(
            """
            CREATE TABLE summary_tasks (
                id TEXT PRIMARY KEY,
                sumdocId TEXT,
                status TEXT,
                errorMessage TEXT,
                model TEXT,
                summary TEXT,
                retryCount INTEGER,
                createdAt TEXT,
                updatedAt TEXT
            )
            """
        )

        # Insert dummy records
        summary_tasks = [
            {
                "id": str(uuid.uuid4()),
                "sumdocId": "76987e4a-0e71-498c-a686-4090185e5215",
                "status": "dummy-document-1",
                "errorMessage": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla at lobortis velit, vel commodo eros. Aliquam tincidunt justo sit amet nulla cursus, at finibus leo mattis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed pellentesque ante a enim scelerisque vestibulum. Duis ut eros eget libero ullamcorper aliquet. Fusce risus ipsum, mattis eu tristique non, dapibus nec arcu. Vivamus commodo interdum mi, eu convallis diam malesuada eu. Nam fringilla orci elit, vitae vehicula turpis posuere nec. Fusce facilisis nibh at ex efficitur, eget laoreet odio tincidunt. Fusce vitae facilisis odio, et semper est. Donec in interdum mi. Donec non sagittis orci. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Duis eu lectus imperdiet, suscipit nisl nec, maximus nisl.",
                "model": "Model A",
                "summary": "Summary A",
                "createdAt": "2024-03-12T12:00:00",
                "updatedAt": "2024-03-12T12:00:00"
            },
            # Dummy Sumdoc 2
            {
                "id": str(uuid.uuid4()),
                "sumdocId": "76987e4a-0e71-498c-a686-4090185e5215",
                "status": "dummy-document-1",
                "errorMessage": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla at lobortis velit, vel commodo eros. Aliquam tincidunt justo sit amet nulla cursus, at finibus leo mattis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed pellentesque ante a enim scelerisque vestibulum. Duis ut eros eget libero ullamcorper aliquet. Fusce risus ipsum, mattis eu tristique non, dapibus nec arcu. Vivamus commodo interdum mi, eu convallis diam malesuada eu. Nam fringilla orci elit, vitae vehicula turpis posuere nec. Fusce facilisis nibh at ex efficitur, eget laoreet odio tincidunt. Fusce vitae facilisis odio, et semper est. Donec in interdum mi. Donec non sagittis orci. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Duis eu lectus imperdiet, suscipit nisl nec, maximus nisl.",
                "model": "Model B",
                "summary": "Summary B",
                "createdAt": "2024-03-12T12:00:00",
                "updatedAt": "2024-03-12T12:00:00"
            }
        ]

        # Insert dummy records into the Sumdocs table
        for summary_task in summary_tasks:
            await database.execute(SummaryTask.__table__.insert().values(summary_task))

@router.post("/summary_tasks/", response_model=SummaryTaskSchema)
async def create_summary_task(summary_task: SummaryTaskSchema):
    # Create a summary task in the DB and enqueue a Celery task
    pass

@router.get("/summary_tasks/{task_id}", response_model=SummaryTaskSchema)
async def get_summary_task(task_id: str):
    # Retrieve a specific summary task by ID
    pass

@router.websocket("/ws/summary_tasks/{task_id}")
async def websocket_summary_task(websocket: WebSocket, task_id: str):
    # Handle WebSocket connection for real-time updates of a summary task
    await websocket.accept()
    while True:
        # logic to send data to the client
        await websocket.send_json({"status": "update"})
    await websocket.close()