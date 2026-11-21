import pytest

from src.Core.Config import Settings
from src.Core.Models.SniperSignal import SniperSignal, Venue
from src.Core.Processors.RugFilter import RugFilter


class _FakeRpc:
    def __init__(self, info):
        self._info = info

    async def get_mint_info(self, mint: str):
        return self._info


class _Info:
    def __init__(self, mint_authority=None, freeze_authority=None, liquidity_sol=10.0, top10=20):
        self.mint_authority = mint_authority
        self.freeze_authority = freeze_authority
        self.liquidity_sol = liquidity_sol
        self.top10_holders_pct = top10


@pytest.mark.asyncio
async def test_rug_filter_rejects_live_mint_authority():
    rf = RugFilter(Settings(require_mint_authority_revoked=True))
    signal = SniperSignal(mint="abc", venue=Venue.PUMPFUN, slot=1, signature="x")
    ok = await rf.passes(signal, _FakeRpc(_Info(mint_authority="someone")))
    assert ok is False


@pytest.mark.asyncio
async def test_rug_filter_accepts_clean_mint():
    rf = RugFilter(Settings())
    signal = SniperSignal(mint="abc", venue=Venue.PUMPFUN, slot=1, signature="x")
    ok = await rf.passes(signal, _FakeRpc(_Info()))
    assert ok is True
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>