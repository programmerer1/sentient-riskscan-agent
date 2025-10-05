import httpx
from .config import SCORECHAIN_API_BASE_URL, SCORECHAIN_API_KEY

class ScorechainClient:
    async def check_wallet(self, address: str):
        if not SCORECHAIN_API_BASE_URL or not SCORECHAIN_API_KEY:
            return {}

        url = f"{SCORECHAIN_API_BASE_URL}/v1/addresses/{address}"
        headers = {"X-API-Key": SCORECHAIN_API_KEY}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
            return resp.json()
