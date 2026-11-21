"""Worker pipeline: queues SniperSignals, runs processors, dispatches to executor."""
from __future__ import annotations

import asyncio
from loguru import logger

from src.Core.Config import Settings
from src.Core.Models.SniperSignal import SniperSignal
from src.Core.Models.TradeIntent import TradeIntent
from src.Core.Processors.RugFilter import RugFilter
from src.Core.Processors.SlippageCalc import SlippageCalc
from src.Infrastructure.Rpc.RpcPool import RpcPool
from src.Infrastructure.Signing.LocalSigner import LocalSigner
from src.Infrastructure.Tx.SendExecutor import SendExecutor


class SniperPipeline:
    def __init__(self, settings: Settings, rpc: RpcPool, signer: LocalSigner) -> None:
        self._settings = settings
        self._rpc = rpc
        self._signer = signer
        self._queue: asyncio.Queue[SniperSignal] = asyncio.Queue(maxsize=512)
        self._rug_filter = RugFilter(settings)
        self._slippage = SlippageCalc(settings)
        self._executor = SendExecutor(settings, rpc, signer)
        self._workers: list[asyncio.Task[None]] = []

    async def start(self, workers: int = 4) -> None:
        for i in range(workers):
            self._workers.append(asyncio.create_task(self._worker(i)))
        logger.info("pipeline started with {} workers", workers)

    async def enqueue(self, signal: SniperSignal) -> None:
        try:
            self._queue.put_nowait(signal)
        except asyncio.QueueFull:
            logger.warning("pipeline queue full, dropping mint={}", signal.mint)

    async def _worker(self, wid: int) -> None:
        while True:
            signal = await self._queue.get()
            try:
                await self._handle(signal)
            except Exception as exc:  # noqa: BLE001
                logger.exception("worker {} failed on {}: {}", wid, signal.mint, exc)
            finally:
                self._queue.task_done()

    async def _handle(self, signal: SniperSignal) -> None:
        if not await self._rug_filter.passes(signal, self._rpc):
            logger.info("rug filter rejected {}", signal.mint)
            return
        intent = TradeIntent(
            mint=signal.mint,
            venue=signal.venue,
            amount_lamports=int(self._settings.snipe_amount_sol * 1_000_000_000),
            slippage_bps=self._settings.max_slippage_bps,
        )
        await self._executor.submit(intent)