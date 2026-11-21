from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field


class Venue(str, Enum):
    PUMPFUN = "pumpfun"
    RAYDIUM = "raydium"
    ORCA = "orca"
    METEORA = "meteora"


class SniperSignal(BaseModel):
    """Emitted by an ingest handler when a new pool / mint is spotted."""

    mint: str
    venue: Venue
    slot: int
    signature: str
    detected_at_ms: int = Field(default=0)

    def age_ms(self, now_ms: int) -> int:
        return max(0, now_ms - self.detected_at_ms)