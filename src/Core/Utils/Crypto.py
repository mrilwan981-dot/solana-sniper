"""Keypair redaction helpers so we never log raw secret keys."""
from __future__ import annotations


def redact_keypair(b58: str) -> str:
    if not b58:
        return "<empty>"
    if len(b58) <= 8:
        return "*" * len(b58)
    return f"{b58[:4]}...{b58[-4:]}"


def redact_sig(sig: str) -> str:
    if len(sig) <= 10:
        return sig
    return f"{sig[:6]}..{sig[-4:]}"