from openai import OpenAI
import os
import asyncio
from fastapi import APIRouter
import os
router = APIRouter()

api_key=os.environ.get("OPENAI_API_KEY")

async def heartbeat(api_key):
    try:
        client = OpenAI(api_key=api_key)
        
        # Run the synchronous OpenAI client code in an executor
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "user", "content": "This is a test"}],
            temperature=0
        )
        return {"status": "API key is valid", "response": response.choices[0].message.content}
    except Exception as e:
        return {"status": "Failed to validate API key", "error": str(e)}
    

@router.get("/heartbeat", tags=["Utilities"])
async def heartbeat_endpoint():
    result = await heartbeat(api_key)
    return(result)