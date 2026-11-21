from __future__ import annotations

from src.Core.Config import Settings


class SlippageCalc:
    """Turns a human slippage bps into a min_out given a quoted amount."""

    def __init__(self, settings: Settings) -> None:
        self._s = settings

    def min_out(self, quoted_out_lamports: int, bps_override: int | None = None) -> int:
        bps = bps_override if bps_override is not None else self._s.max_slippage_bps
        bps = max(0, min(bps, 9_999))
        return quoted_out_lamports * (10_000 - bps) // 10_000

    def apply_priority(self, base_fee_microlamports: int) -> int:
        return max(base_fee_microlamports, self._s.priority_fee_microlamports)