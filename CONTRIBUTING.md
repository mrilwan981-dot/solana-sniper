# Contributing to solana-sniper

Thanks for wanting to help build the fastest Solana sniper bot in the community. Read this before opening a PR.

## Code of Conduct

Be decent. No drama, no scamming, no "I'll run this for you for a fee" DMs. This repo is for educational / research purposes.

## How to contribute

1. Fork the repo and create a feature branch: `git checkout -b feature/jito-bundle-sender`
2. Keep modules small. One processor per file under `src/Core/Processors/`.
3. Add a unit test in `tests/` for anything that touches bonding curve math or fee calculation.
4. Run `python -m pytest tests/` and `python -m ruff check src/` before pushing.
5. Open a PR with a short description of the strategy / handler you touched.

## What we're looking for

- Faster websocket subscription handlers (`src/App/Handlers/`)
- Alternative RPC pool implementations (`src/Infrastructure/Rpc/`)
- Risk filters for rug detection (`src/Core/Processors/RugFilter.py`)
- Jito bundle integration improvements
- Better docs in `docs/`

## What we don't want

- "Profits guaranteed" strategies
- Anything that drains other people's wallets
- Hardcoded private keys (use `.env`, see `.env.example`)

## Style

- Python 3.11+, type hints everywhere
- 4 spaces, ruff-formatted
- Loguru for logging, no `print()` in `src/`