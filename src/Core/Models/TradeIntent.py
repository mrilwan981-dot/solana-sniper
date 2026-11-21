from __future__ import annotations

from pydantic import BaseModel

from src.Core.Models.SniperSignal import Venue


class TradeIntent(BaseModel):
    """A fully-formed buy we want the executor to land."""

    mint: str
    venue: Venue
    amount_lamports: int
    slippage_bps: int
    priority_fee_microlamports: int = 50_000
    jito_tip_lamports: int = 10_000
    dry_run: bool = True

    def effective_fee_lamports(self) -> int:
        return self.jito_tip_lamports + (self.priority_fee_microlamports // 1000)