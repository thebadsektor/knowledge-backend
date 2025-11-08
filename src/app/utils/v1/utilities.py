from openai import OpenAI, APIStatusError, AuthenticationError
import os
import asyncio
from fastapi import APIRouter
import os
router = APIRouter()

api_key=os.environ.get("OPENAI_API_KEY")

async def heartbeat(api_key):
    from openai import OpenAI
    import asyncio

    try:
        client = OpenAI(api_key=api_key)

        # Get models (in a background thread)
        models = await asyncio.to_thread(client.models.list)
        available_models = [m.id for m in models.data]

        # Pick a chat-compatible model
        preferred_models = [
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4-turbo",
            "gpt-3.5-turbo"
        ]
        model = next((m for m in preferred_models if m in available_models), None)

        if not model:
            raise ValueError("No chat-compatible model found in available models.")

        # Test the model with a simple completion
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=model,
            messages=[{"role": "user", "content": "Hello"}],
            temperature=0
        )

        return {
            "status": "API key is valid",
            "model": model,
            "response": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "status": "OpenAI API returned an error",
            "error": str(e)
        }
    

@router.get("/heartbeat", tags=["Utilities"])
async def heartbeat_endpoint():
    result = await heartbeat(api_key)
    return(result)