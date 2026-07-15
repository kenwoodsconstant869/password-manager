"""Frameworks & Drivers : implémentation Fernet du chiffrement."""

from cryptography.fernet import Fernet

from src.application.interfaces.encryption_service import EncryptionService


class FernetEncryptionService(EncryptionService):

    def __init__(self, key: bytes):
        self._fernet = Fernet(key)

    def encrypt(self, plain_text: str) -> str:
        return self._fernet.encrypt(plain_text.encode()).decode()

    def decrypt(self, cipher_text: str) -> str:
        return self._fernet.decrypt(cipher_text.encode()).decode()

    @staticmethod
    def generate_key() -> bytes:
        return Fernet.generate_key()
