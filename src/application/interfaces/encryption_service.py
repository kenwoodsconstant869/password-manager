"""Port pour le chiffrement/déchiffrement des mots de passe."""

from abc import ABC, abstractmethod


class EncryptionService(ABC):

    @abstractmethod
    def encrypt(self, plain_text: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, cipher_text: str) -> str:
        raise NotImplementedError
