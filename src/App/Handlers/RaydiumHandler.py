"""Watches Raydium AMM init logs and forwards them to the pipeline."""
from __future__ import annotations

from loguru import logger

from src.Core.Models.SniperSignal import SniperSignal, Venue
from src.Core.Pipeline import SniperPipeline
from src.Infrastructure.Rpc.RpcPool import RpcPool

RAYDIUM_AMM_V4 = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"


class RaydiumHandler:
    def __init__(self, rpc: RpcPool, pipeline: SniperPipeline) -> None:
        self._rpc = rpc
        self._pipeline = pipeline

    async def start(self) -> None:
        logger.info("subscribing to raydium amm_v4 logs")
        async for log in self._rpc.logs_mentions([RAYDIUM_AMM_V4]):
            if log.err:
                continue
            if not any("initialize2" in line for line in log.logs):
                continue
            signal = SniperSignal(
                mint="pending-resolve",
                venue=Venue.RAYDIUM,
                slot=log.slot,
                signature=str(log.signature),
            )
            await self._pipeline.enqueue(signal)