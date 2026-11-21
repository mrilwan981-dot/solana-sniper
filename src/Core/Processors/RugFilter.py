"""Cheap pre-trade checks: mint authority, top-10 concentration, liquidity."""
from __future__ import annotations

from loguru import logger

from src.Core.Config import Settings
from src.Core.Models.SniperSignal import SniperSignal
from src.Infrastructure.Rpc.RpcPool import RpcPool


class RugFilter:
    def __init__(self, settings: Settings) -> None:
        self._s = settings

    async def passes(self, signal: SniperSignal, rpc: RpcPool) -> bool:
        if signal.mint.startswith("pending"):
            logger.debug("skipping unresolved mint signal")
            return False

        info = await rpc.get_mint_info(signal.mint)
        if info is None:
            return False

        if self._s.require_mint_authority_revoked and info.mint_authority is not None:
            logger.info("{} has live mint authority", signal.mint)
            return False

        if info.freeze_authority is not None:
            logger.info("{} has live freeze authority", signal.mint)
            return False

        if info.liquidity_sol < self._s.min_liquidity_sol:
            logger.info("{} liquidity too thin: {} SOL", signal.mint, info.liquidity_sol)
            return False

        if info.top10_holders_pct > self._s.max_top10_holders_pct:
            logger.info("{} top10 concentration {}%", signal.mint, info.top10_holders_pct)
            return False

        return True