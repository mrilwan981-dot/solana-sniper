"""Subscribes to pump.fun program logs and emits a SniperSignal on new mints."""
from __future__ import annotations

import base58
from loguru import logger

from src.Core.Models.SniperSignal import SniperSignal, Venue
from src.Core.Pipeline import SniperPipeline
from src.Infrastructure.Rpc.RpcPool import RpcPool

PUMPFUN_PROGRAM = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"


class PumpFunHandler:
    def __init__(self, rpc: RpcPool, pipeline: SniperPipeline) -> None:
        self._rpc = rpc
        self._pipeline = pipeline

    async def start(self) -> None:
        logger.info("subscribing to pump.fun logs")
        async for log in self._rpc.logs_mentions([PUMPFUN_PROGRAM]):
            if log.err:
                continue
            for raw in log.logs:
                if "Program log: Instruction: InitializeMint" not in raw:
                    continue
                try:
                    mint = self._extract_mint(log.logs)
                except Exception as exc:  # noqa: BLE001
                    logger.debug("pumpfun parse failed: {}", exc)
                    continue
                signal = SniperSignal(
                    mint=mint,
                    venue=Venue.PUMPFUN,
                    slot=log.slot,
                    signature=base58.b58encode(log.signature).decode(),
                )
                await self._pipeline.enqueue(signal)

    @staticmethod
    def _extract_mint(logs: list[str]) -> str:
        for line in logs:
            if line.startswith("Program log: Mint: "):
                return line.split("Mint: ", 1)[1].strip()
        raise ValueError("no mint in logs")