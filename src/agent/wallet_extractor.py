import json
import httpx
from .config import SUPPORTED_NETWORKS, EXTRACTOR_MODEL_API_URL, EXTRACTOR_MODEL_NAME, EXTRACTOR_MODEL_API_KEY
from .prompts.extractor import SYSTEM_PROMPT_TEMPLATE

class WalletExtractor:
    async def extract(self, prompt: str) -> tuple[str | None, str | None]:
        headers = {
            "Authorization": f"Bearer {EXTRACTOR_MODEL_API_KEY}",
            "Content-Type": "application/json"
        }

        system_instruction = {
            "role": "system",
            "content": SYSTEM_PROMPT_TEMPLATE.format(supported_networks=SUPPORTED_NETWORKS)
        }
        
        payload = {
            "model": EXTRACTOR_MODEL_NAME,
            "max_tokens" : 800,
            "top_p" : 1,
            #"top_k" : 40,
            "presence_penalty" : 0,
            "frequency_penalty" : 0,
            "temperature" : 0.0,
            "messages": [
                system_instruction,
                {"role": "user", "content": prompt}
            ]
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(EXTRACTOR_MODEL_API_URL, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        try:
            content = (
                data.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "{}")
            )
            parsed = json.loads(content)
            return parsed.get("address"), parsed.get("network")
        except Exception:
            return None, None
