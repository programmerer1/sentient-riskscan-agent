import httpx
import json
from .config import MODEL_API_URL, MODEL_NAME, MODEL_API_KEY
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ResponseFormatter:
    async def format(self, network: str, address: str, result: dict, user_prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {MODEL_API_KEY}",
            "Content-Type": "application/json"
        }

        system_instruction = {
            "role": "system",
            "content": f"""
You are an assistant that transforms blockchain wallet analysis results into a professional, detailed, user-friendly report in Markdown.

Date today: {datetime.utcnow().strftime('%Y-%m-%d')}

Requirements:
- Always write the report in the same language as the user's original query.
- Use Markdown headings, bullet points, and tables where useful.
- Always include:
  * The wallet address
  * The blockchain/network
  * Risk score and category
  * Any tags, labels, or sanctions flags
- Provide a short explanation of what the risk score means for a regular user.
- **IMPORTANT**: Do NOT output raw JSON. Only text, only human-friendly insights.
- Always add a list of sources and the following text at the end: This report is for informational purposes only and does not constitute legal or financial advice. Always conduct due diligence when interacting with blockchain addresses.

---

### Additional logic for interpreting **Anchain** results

If **Anchain data is available** and it shows:
- `risk_score = 50`
- `risk_level = Guarded`
- and **neither the Anchain report nor other analytical sources indicate any specific suspicious or illegal activities**, such as:
  - fraud, scam, or phishing
  - money laundering
  - hacking, exploit, or attack-related activity
  - darknet or marketplace involvement
  - sanctions or blacklist association
  - mixing or tumbling services
  - or any **other unlawful or suspicious operations**

then:

1. **Do not treat the "Guarded" level as a serious risk.**
2. **Do not highlight it as a negative or alarming signal.**
3. Instead, include a short neutral clarification such as:

   > The Anchain service assigned a “Guarded” (moderate) risk level.  
   > This rating is commonly applied to new or low-activity wallets and **does not indicate any confirmed suspicious behavior**.  
   > No fraudulent or illicit transactions were detected. The current risk level can be considered **moderate and non-critical**.
"""
        }

        user_message = {
            "role": "user",
            "content": f"""
Wallet Analysis Report

User original query: {user_prompt};
Network: {network};
Address: {address};

Raw API Data:
{result}
"""
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
