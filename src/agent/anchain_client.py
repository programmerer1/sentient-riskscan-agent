import httpx
from .config import ANCHAIN_API_BASE_URL, ANCHAIN_API_KEY

class AnchainClient:
    async def check_wallet(self, network: str, address: str, action: str="activity"):
        if not ANCHAIN_API_BASE_URL or not ANCHAIN_API_KEY:
            return {}

        url = f"{ANCHAIN_API_BASE_URL}/crypto_screening?protocol={network}&address={address}&action={action}"
        headers = {"Authorization": f"Bearer {ANCHAIN_API_KEY}"}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
            json_resp = resp.json()

            if json_resp.get("status") != 200:
                raise ValueError(json_resp)

            if json_resp.get("err_msg"):
                raise ValueError(json_resp.get("err_msg"))
            
            original_data = json_resp.get("data", {})
            
            filtered_data = {
                "protocol": original_data.get("protocol"),
                "address": original_data.get("address"),
                "entity_type": original_data.get("entity_type"),
                "risk_score": original_data.get("risk_score"),
                "risk_level": original_data.get("risk_level")
            }
            
            categories_to_exclude = ["exchange", "whale", "wallet", "miner", "contract"]

            if "risk_activity" in original_data:
                filtered_activities = []
                for activity in original_data["risk_activity"]:
                    activity_category = activity.get("category")
                    
                    if activity_category in categories_to_exclude:
                        continue
                        
                    filtered_activity = {
                        "description": activity.get("description"),
                        "category": activity.get("category"), 
                        "transaction_count": activity.get("txn_cnt") 
                    }

                    filtered_activities.append(filtered_activity)
                    
                filtered_data["risk_activity"] = filtered_activities
            else:
                filtered_data["address_description"] = "No suspicious transactions were detected on this wallet."

            return filtered_data
