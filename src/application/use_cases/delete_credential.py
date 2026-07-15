"""Use case: supprimer un Credential."""

from dataclasses import dataclass

from src.application.interfaces.credential_repository import CredentialRepository
from src.domain.exceptions.credential_exceptions import InvalidCredentialError


@dataclass
class DeleteCredentialInput:
    credential_id: int


class DeleteCredentialUseCase:

    def __init__(self, repository: CredentialRepository):
        self._repository = repository

    def execute(self, input_data: DeleteCredentialInput) -> None:
        credential = self._repository.get_by_id(input_data.credential_id)
        if credential is None:
            raise InvalidCredentialError(f"Aucun credential trouvé avec l'id {input_data.credential_id}.")
        self._repository.delete(input_data.credential_id)
