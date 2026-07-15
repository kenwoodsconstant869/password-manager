"""Use case: créer un nouveau Credential."""

from dataclasses import dataclass

from src.application.interfaces.credential_repository import CredentialRepository
from src.application.interfaces.encryption_service import EncryptionService
from src.domain.entities.credential import Credential


@dataclass
class CreateCredentialInput:
    service: str
    username: str
    password: str


@dataclass
class CreateCredentialOutput:
    id: int
    service: str
    username: str


class CreateCredentialUseCase:

    def __init__(self, repository: CredentialRepository, encryption: EncryptionService):
        self._repository = repository
        self._encryption = encryption

    def execute(self, input_data: CreateCredentialInput) -> CreateCredentialOutput:
        credential = Credential(
            service=input_data.service,
            username=input_data.username,
            password=input_data.password,
        )
        credential.password = self._encryption.encrypt(credential.password)
        saved = self._repository.add(credential)
        return CreateCredentialOutput(id=saved.id, service=saved.service, username=saved.username)
