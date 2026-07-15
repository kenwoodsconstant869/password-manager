"""Use case: mettre à jour un Credential existant."""

from dataclasses import dataclass

from src.application.interfaces.credential_repository import CredentialRepository
from src.application.interfaces.encryption_service import EncryptionService
from src.domain.exceptions.credential_exceptions import InvalidCredentialError


@dataclass
class UpdateCredentialInput:
    credential_id: int
    new_service: str | None = None
    new_password: str | None = None


class UpdateCredentialUseCase:

    def __init__(self, repository: CredentialRepository, encryption: EncryptionService):
        self._repository = repository
        self._encryption = encryption

    def execute(self, input_data: UpdateCredentialInput) -> None:
        credential = self._repository.get_by_id(input_data.credential_id)
        if credential is None:
            raise InvalidCredentialError(f"Aucun credential trouvé avec l'id {input_data.credential_id}.")

        if input_data.new_service is not None:
            credential.rename_service(input_data.new_service)

        if input_data.new_password is not None:
            credential.update_password(input_data.new_password)
            credential.password = self._encryption.encrypt(credential.password)

        self._repository.update(credential)
