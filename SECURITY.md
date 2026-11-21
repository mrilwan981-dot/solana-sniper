# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.4.x   | :white_check_mark: |
| 0.3.x   | :x:                |
| < 0.3   | :x:                |

## Reporting a Vulnerability

If you find a vulnerability in solana-sniper — e.g. private key leakage via logs, unsafe RPC deserialization, or a path where the bot could be tricked into signing a malicious transaction — **do not open a public issue**.

Open a private security advisory on GitHub or email `security@sniper-builders.dev` (PGP key in `docs/pgp.txt`).

We aim to acknowledge within 48 hours and ship a patch within 7 days.

## Handling of keypairs

- Never commit `.keypair.json` or `.env` files. `.gitignore` blocks them.
- The `LocalSigner` (`src/Infrastructure/Signing/LocalSigner.py`) zeroes secret buffers in `close()`.
- Never log the raw secret key. `redact_keypair()` in `src/Core/Utils/Crypto.py` enforces this.
- Run the bot on a dedicated hot wallet with only the funds you're willing to lose.

## Threat model

solana-sniper talks to untrusted RPC endpoints and untrusted token mints. We assume:
- RPC providers may lie about slot heights / logs
- Token mints may be honeypots or rug pulls
- MEV bots will front-run you

## Disclaimer

This software is provided for educational and research purposes only. Use at your own risk. Do not use on mainnet with funds you cannot afford to lose.