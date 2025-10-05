import json
import logging
from typing import Any

from sentient_agent_framework.interface.agent import AbstractAgent
from sentient_agent_framework.interface.request import Query
from sentient_agent_framework.interface.session import Session
from sentient_agent_framework.interface.response_handler import ResponseHandler

from .wallet_extractor import WalletExtractor
from .anchain_client import AnchainClient
from .scorechain_client import ScorechainClient
from .chainalysis_client import ChainalysisClient
from .response_formatter import ResponseFormatter
from .config import SUPPORTED_NETWORKS
from .mysql_connector import MySQLConnector
from .mysql_cache import MySQLCache

logger = logging.getLogger(__name__)

class Agent(AbstractAgent):
    def __init__(self, name: str = "Risk Scan"):
        super().__init__(name)
        self.wallet_extractor = WalletExtractor()
        self.scorechain_client = ScorechainClient()
        self.chainalysis_client = ChainalysisClient()
        self.anchain_client = AnchainClient()
        self.formatter = ResponseFormatter()
        self.mysql_connector = MySQLConnector()
        self.mysql_cache = MySQLCache(self.mysql_connector, default_ttl_hours=1)

    async def assist(self, session: Session, query: Query, response_handler: ResponseHandler) -> None:
        try:
            prompt = getattr(query, "prompt", "") or ""
            if not prompt:
                await response_handler.emit_error("Empty prompt", details={"field": "prompt"})
                return

            address, network = await self.wallet_extractor.extract(prompt)

            if not address or not network:
                await response_handler.emit_error(
                    f"Sorry, you must specify both a valid wallet address and a supported network. Please repeat your query including both. Supported networks: {SUPPORTED_NETWORKS}",details={"field": "prompt"}
                )
                return

            cache_key = f"{network}:{address}"
            result = await self.mysql_cache.get(cache_key)

            if not result:
                scorechain_result = await self.scorechain_client.check_wallet(address)
                if scorechain_result:
                    result['scorechain_data'] = scorechain_result

                chainalysis_result = await self.chainalysis_client.check_wallet(address)
                if chainalysis_result:
                    result['chainalysis_data'] = chainalysis_result

                anchain_result = await self.anchain_client.check_wallet(network, address)
                if anchain_result:
                    result['anchain_data'] = anchain_result

                await self.mysql_cache.set(cache_key, json.dumps(result))

            report = await self.formatter.format(network, address, json.dumps(result, indent=2), prompt)
            await response_handler.respond("response", report)
        except Exception as exc:
            logger.error("Something went wrong.", exc_info=True)
            await response_handler.emit_error(
                "Something went wrong. Please try again later.",
                details={"stage": "respond", "error_type": type(exc).__name__}
            )
            
        finally:
            await response_handler.complete()
            await self.mysql_connector.close_pool()
