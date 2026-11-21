"""Entry point: wires up config, RPC pool, ingest handlers and the worker pipeline."""
from __future__ import annotations

import asyncio
from loguru import logger

from src.App.Handlers.PumpFunHandler import PumpFunHandler
from src.App.Handlers.RaydiumHandler import RaydiumHandler
from src.Core.Config import load_settings
from src.Core.Pipeline import SniperPipeline
from src.Infrastructure.Rpc.RpcPool import RpcPool
from src.Infrastructure.Signing.LocalSigner import LocalSigner


async def _amain() -> None:
    settings = load_settings()
    logger.info("booting solana-sniper v{} dry_run={}", "0.4.2", settings.dry_run)

    rpc = RpcPool(settings.rpc_endpoints, settings.rpc_wss)
    await rpc.start()

    signer = LocalSigner(settings.wallet_keypair_path)
    pipeline = SniperPipeline(settings=settings, rpc=rpc, signer=signer)

    handlers = [
        PumpFunHandler(rpc=rpc, pipeline=pipeline),
        RaydiumHandler(rpc=rpc, pipeline=pipeline),
    ]

    try:
        await asyncio.gather(*(h.start() for h in handlers))
    finally:
        await rpc.close()
        signer.close()


def main() -> None:
    try:
        asyncio.run(_amain())
    except KeyboardInterrupt:
        logger.warning("interrupted — shutting down")


if __name__ == "__main__":
    main()