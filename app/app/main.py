from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Float, Boolean, JSON, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from typing import List
from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()
from .models.models import Sumdoc
from .schemas.schemas import ProductSchema, SumdocSchema
from .database.database import database
# from .routes import products
from .api.v1 import summaries
from typing import List, Dict, Any
import asyncio

# Define the FastAPI app
app = FastAPI()

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
app.include_router(summaries.router, prefix="/api/v1/summaries")


@app.get("/heartbeat")
async def heartbeat():
    try:
        client = OpenAI()
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
          model="gpt-3.5-turbo-0613",
          messages=[{"role": "user", "content": "This is a test"}],
          temperature=0
        )
        return("API key is valid. Received response:", response.choices[0].message.content)
    except Exception as e:
        return("Failed to validate API key. Error:", str(e))