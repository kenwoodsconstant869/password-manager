"""Use case: lister tous les Credential (avec mot de passe déchiffré)."""

from dataclasses import dataclass

from src.application.interfaces.credential_repository import CredentialRepository
from src.application.interfaces.encryption_service import EncryptionService


@dataclass
class CredentialListItem:
    id: int
    service: str
    username: str
    password: str
    created_at: str


class ListCredentialsUseCase:

    def __init__(self, repository: CredentialRepository, encryption: EncryptionService):
        self._repository = repository
        self._encryption = encryption

    def execute(self) -> list[CredentialListItem]:
        credentials = self._repository.get_all()
        return [
            CredentialListItem(
                id=c.id,
                service=c.service,
                username=c.username,
                password=self._encryption.decrypt(c.password),
                created_at=c.created_at.isoformat(),
            )
            for c in credentials
        ]
