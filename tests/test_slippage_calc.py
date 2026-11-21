from src.Core.Config import Settings
from src.Core.Processors.SlippageCalc import SlippageCalc


def test_min_out_1500bps():
    s = Settings(max_slippage_bps=1500)
    calc = SlippageCalc(s)
    assert calc.min_out(1_000_000) == 850_000


def test_min_out_zero_slippage():
    s = Settings(max_slippage_bps=0)
    calc = SlippageCalc(s)
    assert calc.min_out(1_000_000) == 1_000_000


def test_priority_floor():
    s = Settings(priority_fee_microlamports=50_000)
    calc = SlippageCalc(s)
    assert calc.apply_priority(10_000) == 50_000