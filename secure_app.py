"""
HARDENED LOCAL DEMO

A safer rewrite of insecure_app.py for a secure-code review exercise.
"""

import hashlib
import hmac
import json
import os
import subprocess
import sys
from typing import Any


ITERATIONS = 310_000
ALLOWED_DIAGNOSTICS = {
    "python_version": [sys.executable, "--version"],
}


def hash_password(password: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
    """Use PBKDF2-HMAC-SHA256 with a unique random salt."""
    safe_salt = salt or os.urandom(16)
    derived_key = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), safe_salt, ITERATIONS
    )
    return safe_salt, derived_key


def verify_password(password: str, salt: bytes, expected_hash: bytes) -> bool:
    """Compare password hashes using a timing-safe comparison."""
    _, candidate_hash = hash_password(password, salt)
    return hmac.compare_digest(candidate_hash, expected_hash)


def load_preferences(serialized_data: str) -> dict[str, Any]:
    """Use JSON for data exchange and validate the expected structure."""
    parsed = json.loads(serialized_data)
    if not isinstance(parsed, dict):
        raise ValueError("Preferences must be a JSON object.")
    return parsed


def run_allowed_diagnostic(name: str) -> str:
    """Run only an allow-listed command without invoking a shell."""
    command = ALLOWED_DIAGNOSTICS.get(name)
    if command is None:
        raise ValueError("Unsupported diagnostic requested.")

    result = subprocess.run(
        command,
        shell=False,
        text=True,
        capture_output=True,
        check=True,
        timeout=10,
    )
    return result.stdout.strip()
