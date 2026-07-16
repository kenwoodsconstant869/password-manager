from src.application.interfaces.encryption_service import EncryptionService


class InMemoryEncryptionService(EncryptionService):
    def encrypt(self, plain_text: str) -> str:
        return plain_text

    def decrypt(self, cipher_text: str) -> str:
        return cipher_text
