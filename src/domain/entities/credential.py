from datetime import datetime
from src.domain.exceptions.credential_exceptions import InvalidCredentialError


class Credential:
    """Représente une entrée de mot de passe (service, identifiant, mot de passe)."""

    def __init__(
        self,
        service: str,
        username: str,
        password: str,
        id: int = None,
        created_at: datetime = None,
    ):
        self.id = id
        self.service = self._validate_service(service)
        self.username = self._validate_username(username)
        self.password = self._validate_password(password)
        self.created_at = created_at or datetime.now()

    @staticmethod
    def _validate_service(service: str) -> str:
        if not service or not service.strip():
            raise InvalidCredentialError("Le nom du service ne peut pas être vide.")
        return service.strip()

    @staticmethod
    def _validate_username(username: str) -> str:
        if not username or not username.strip():
            raise InvalidCredentialError("Le nom d'utilisateur ne peut pas être vide.")
        return username.strip()

    @staticmethod
    def _validate_password(password: str) -> str:
        if not password or len(password) < 4:
            raise InvalidCredentialError("Le mot de passe doit contenir au moins 4 caractères.")
        return password

    def update_password(self, new_password: str) -> None:
        self.password = self._validate_password(new_password)

    def rename_service(self, new_service: str) -> None:
        self.service = self._validate_service(new_service)

    def matches(self, keyword: str) -> bool:
        keyword = keyword.lower()
        return keyword in self.service.lower() or keyword in self.username.lower()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "service": self.service,
            "username": self.username,
            "password": self.password,
            "created_at": self.created_at.isoformat(),
        }

    def __eq__(self, other):
        if not isinstance(other, Credential):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"Credential(id={self.id}, service='{self.service}', username='{self.username}')"
