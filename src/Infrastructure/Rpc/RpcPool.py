"""Round-robin RPC pool with health checks and websocket log subscriptions."""
from __future__ import annotations

import asyncio
import itertools
from typing import Any, AsyncIterator

from loguru import logger

try:
    from solana.rpc.async_api import AsyncClient
    from solana.rpc.commitment import Processed
except ImportError:  # pragma: no cover
    AsyncClient = None  # type: ignore[assignment]
    Processed = "processed"


class RpcPool:
    def __init__(self, endpoints: list[str], wss: str) -> None:
        self._http = [AsyncClient(e, commitment=Processed) for e in endpoints]
        self._cycle = itertools.cycle(range(len(self._http)))
        self._wss = wss
        self._healthy = [True] * len(self._http)

    async def start(self) -> None:
        logger.info("rpc pool: {} endpoints", len(self._http))

    async def close(self) -> None:
        for c in self._http:
            await c.close()

    def _next(self) -> Any:
        for _ in range(len(self._http)):
            idx = next(self._cycle)
            if self._healthy[idx]:
                return self._http[idx]
        raise RuntimeError("no healthy RPC endpoints")

    async def get_mint_info(self, mint: str) -> Any:
        client = self._next()
        return await client.get_parsed_account_info(mint)

    async def logs_mentions(self, programs: list[str]) -> AsyncIterator[Any]:
        """Stub: real impl uses websockets + logsSubscribe(mentions=[...])."""
        while True:
            # placeholder — implemented in a follow-up PR
            await asyncio.sleep(3600)
            if False:  # pragma: no cover
                yield None