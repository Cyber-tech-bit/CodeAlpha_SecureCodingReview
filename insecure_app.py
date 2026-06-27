"""
INTENTIONALLY INSECURE LOCAL DEMO

This file exists only for the CodeAlpha Secure Coding Review task.
Do not deploy it, connect it to a real service, or run it with untrusted input.
"""

import hashlib
import pickle
import subprocess

# Intentionally hard-coded for code-review practice only.
DATABASE_PASSWORD = "demo_password_123"


def create_password_hash(password: str) -> str:
    """Insecure: MD5 is not appropriate for storing passwords."""
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def load_preferences(serialized_data: bytes):
    """Insecure: pickle can execute code during deserialization."""
    return pickle.loads(serialized_data)


def run_diagnostic(command: str) -> str:
    """Insecure: shell=True can allow command injection when input is untrusted."""
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout
