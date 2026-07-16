"""Frameworks & Drivers : implémentation Fernet du chiffrement."""

import os
from pathlib import Path

from cryptography.fernet import Fernet

from src.application.interfaces.encryption_service import EncryptionService


class FernetEncryptionService(EncryptionService):

    def __init__(self, key: bytes | str):
        if isinstance(key, str):
            key = key.encode()
        self._fernet = Fernet(key)

    def encrypt(self, plain_text: str) -> str:
        return self._fernet.encrypt(plain_text.encode()).decode()

    def decrypt(self, cipher_text: str) -> str:
        return self._fernet.decrypt(cipher_text.encode()).decode()

    @staticmethod
    def load_or_create_key(key_path: str | None = None) -> bytes:
        resolved_path = key_path or os.environ.get("PASSWORD_MANAGER_KEY_PATH", ".password_manager.key")
        path = Path(resolved_path)
        if path.exists():
            return path.read_bytes().strip()

        key = Fernet.generate_key()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(key)
        return key

    @staticmethod
    def generate_key() -> bytes:
        return Fernet.generate_key()
