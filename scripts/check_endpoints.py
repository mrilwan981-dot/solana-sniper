"""Pings every configured RPC and reports latency."""
import asyncio
import time

from solana.rpc.async_api import AsyncClient

from src.Core.Config import load_settings


async def _ping(url: str) -> None:
    async with AsyncClient(url) as c:
        t0 = time.perf_counter()
        await c.get_slot()
        print(f"{url}  {int((time.perf_counter() - t0) * 1000)}ms")


async def main() -> None:
    s = load_settings()
    await asyncio.gather(*(_ping(u) for u in s.rpc_list()))


if __name__ == "__main__":
    asyncio.run(main())