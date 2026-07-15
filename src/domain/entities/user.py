import hashlib
import os
from src.domain.exceptions.user_exceptions import InvalidUserError, AuthenticationError


class User:
    """Représente l'utilisateur propriétaire du coffre-fort de mots de passe."""

    def __init__(self, username: str, password_hash: str = None, salt: bytes = None, id: int = None):
        self.id = id
        self.username = self._validate_username(username)
        self.salt = salt or os.urandom(16)
        self.password_hash = password_hash  # None si pas encore défini

    @staticmethod
    def _validate_username(username: str) -> str:
        if not username or not username.strip():
            raise InvalidUserError("Le nom d'utilisateur ne peut pas être vide.")
        return username.strip()

    @classmethod
    def create(cls, username: str, master_password: str) -> "User":
        """Factory method pour créer un nouvel utilisateur avec mot de passe maître."""
        user = cls(username=username)
        user.set_master_password(master_password)
        return user

    def set_master_password(self, master_password: str) -> None:
        if not master_password or len(master_password) < 8:
            raise InvalidUserError("Le mot de passe maître doit contenir au moins 8 caractères.")
        self.password_hash = self._hash_password(master_password, self.salt)

    def verify_password(self, password_attempt: str) -> bool:
        attempt_hash = self._hash_password(password_attempt, self.salt)
        if attempt_hash != self.password_hash:
            raise AuthenticationError("Mot de passe maître incorrect.")
        return True

    @staticmethod
    def _hash_password(password: str, salt: bytes) -> str:
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt, 390_000
        ).hex()

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"
