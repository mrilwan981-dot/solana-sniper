"""Builds, signs and (optionally) broadcasts buy tx via Jito bundle."""
from __future__ import annotations

from loguru import logger

from src.Core.Config import Settings
from src.Core.Models.TradeIntent import TradeIntent
from src.Infrastructure.Rpc.RpcPool import RpcPool
from src.Infrastructure.Signing.LocalSigner import LocalSigner


class SendExecutor:
    def __init__(self, settings: Settings, rpc: RpcPool, signer: LocalSigner) -> None:
        self._s = settings
        self._rpc = rpc
        self._signer = signer

    async def submit(self, intent: TradeIntent) -> str | None:
        if self._s.dry_run:
            logger.info(
                "[dry-run] would buy {} lamports of {} on {}",
                intent.amount_lamports,
                intent.mint,
                intent.venue.value,
            )
            return None

        logger.info("submitting intent mint={} fee={}", intent.mint, intent.effective_fee_lamports())
        # TODO: build swap ix via raydium/pumpfun SDK, sign, sendBundle to jito
        return None