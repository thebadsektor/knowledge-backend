from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Float, Boolean, JSON, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List
from pydantic import BaseModel
import os
from dotenv import load_dotenv
# from .routes import products
from api.v1 import summaries as summaries_v1
from api.v2 import summaries as summaries_v2
from api.v1 import general_tasks
from typing import List, Dict, Any
import asyncio
from openai import OpenAI
from utils.v1 import utilities

load_dotenv()

api_key=os.environ.get("OPENAI_API_KEY")

tags_metadata = [
    {
        "name": "General Tasks",
        "description": "Operations with items. Manage items, search, and more.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://example.com/items-docs",
        },
    },
    {
        "name": "Summaries",
        "description": "Operations with items. Manage items, search, and more.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://example.com/items-docs",
        },
    },
    {
        "name": "Summaries v2",
        "description": "Operations with items. Manage items, search, and more.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://example.com/items-docs",
        },
    },
    {
        "name": "Utilities",
        "description": "Operations with items. Manage items, search, and more.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://example.com/items-docs",
        },
    }
]

# Define the FastAPI app
app = FastAPI(openapi_tags=tags_metadata,
              title='Knowledge Research Inc. API',
              description='Knowledge Research Inc.'
              )

# Configure CORS

origins = [
    "*",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# app.include_router(products.router)
app.include_router(general_tasks.router, prefix="/api/v1/tasks")
app.include_router(summaries_v1.router, prefix="/api/v1/summaries")
app.include_router(summaries_v2.router, prefix="/api/v2/summaries")
app.include_router(utilities.router, prefix="/api/v1/utilities")


# @app.get("/heartbeat", tags=["Utilities"])
# async def heartbeat():
#     try:
#         client = OpenAI()
#         client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
#         response = client.chat.completions.create(
#           model="gpt-3.5-turbo-0613",
#           messages=[{"role": "user", "content": "This is a test"}],
#           temperature=0
#         )
#         return("API key is valid. Received response:", response.choices[0].message.content)
#     except Exception as e:
#         return("Failed to validate API key. Error:", str(e))