"""Loads a keypair from disk and signs transactions. Never logs the secret."""
from __future__ import annotations

import json
from pathlib import Path

from loguru import logger
from solders.keypair import Keypair


class LocalSigner:
    def __init__(self, keypair_path: str) -> None:
        self._path = Path(keypair_path)
        self._kp: Keypair | None = None
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            logger.warning("keypair {} missing — signer disabled", self._path)
            return
        raw = json.loads(self._path.read_text())
        self._kp = Keypair.from_bytes(bytes(raw))
        logger.info("loaded signer pubkey={}", str(self._kp.pubkey()))

    @property
    def pubkey(self) -> str | None:
        return str(self._kp.pubkey()) if self._kp else None

    def sign(self, message: bytes) -> bytes:
        if self._kp is None:
            raise RuntimeError("signer not loaded")
        return bytes(self._kp.sign_message(message))

    def close(self) -> None:
        self._kp = None