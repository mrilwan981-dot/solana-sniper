"""Typed settings loaded from environment / .env."""
from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    rpc_endpoints: str = "https://api.mainnet-beta.solana.com"
    rpc_wss: str = "wss://api.mainnet-beta.solana.com"
    jito_url: str = "https://mainnet.block-engine.jito.wtf/api/v1/bundles"
    jito_tip_lamports: int = 10_000
    wallet_keypair_path: str = "./.wallets/hot.keypair.json"

    snipe_amount_sol: float = 0.05
    max_slippage_bps: int = 1500
    priority_fee_microlamports: int = 50_000
    dry_run: bool = True

    min_liquidity_sol: float = 5.0
    max_top10_holders_pct: int = 45
    require_mint_authority_revoked: bool = True

    def rpc_list(self) -> list[str]:
        return [u.strip() for u in self.rpc_endpoints.split(",") if u.strip()]


def load_settings() -> Settings:
    s = Settings()
    # pydantic doesn't expose rpc_list as a field, expose as property alias
    s.__dict__["rpc_endpoints"] = ",".join(s.rpc_list())
    return s