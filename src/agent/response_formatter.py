import httpx
import json
from .config import MODEL_API_URL, MODEL_NAME, MODEL_API_KEY
from .prompts.formatter import SYSTEM_PROMPT_TEMPLATE, USER_PROMPT_TEMPLATE
from datetime import datetime

class ResponseFormatter:
    async def format(self, network: str, address: str, result: dict, user_prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {MODEL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        system_instruction = {
            "role": "system",
            "content": SYSTEM_PROMPT_TEMPLATE.format(datetime={datetime.utcnow().strftime('%Y-%m-%d')})
        }

        user_message = {
            "role": "user",
            "content": USER_PROMPT_TEMPLATE.format(
                user_prompt=user_prompt,
                network=network,
                address=address,
                result=result
            )
        }

        payload = {
            "model": MODEL_NAME,
            "max_tokens" : 25000,
            "top_p" : 1,
            "top_k" : 40,
            "presence_penalty" : 0,
            "frequency_penalty" : 0,
            "temperature" : 0.0,
            "messages": [
                system_instruction,
                user_message
            ]
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(MODEL_API_URL, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        return (
            data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "Report formatting failed.")
        )
