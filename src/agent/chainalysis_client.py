import httpx
from .config import CHAINALYSIS_API_BASE_URL, CHAINALYSIS_API_KEY

class ChainalysisClient:
    async def check_wallet(self, address: str):
        if not CHAINALYSIS_API_BASE_URL or not CHAINALYSIS_API_KEY:
            return {}

        url = f"{CHAINALYSIS_API_BASE_URL}/v1/address/{address}"
        headers = {"X-API-Key": CHAINALYSIS_API_KEY}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
            return resp.json().get("identifications", {})
