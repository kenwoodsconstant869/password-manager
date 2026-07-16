from src.application.interfaces.credential_repository import CredentialRepository
from src.domain.entities.credential import Credential


class InMemoryCredentialRepository(CredentialRepository):
    def __init__(self) -> None:
        self._items: list[Credential] = []
        self._next_id = 1

    def add(self, credential: Credential) -> Credential:
        credential.id = self._next_id
        self._next_id += 1
        self._items.append(credential)
        return credential

    def get_by_id(self, credential_id: int) -> Credential | None:
        for item in self._items:
            if item.id == credential_id:
                return item
        return None

    def get_all(self) -> list[Credential]:
        return list(self._items)

    def update(self, credential: Credential) -> None:
        for index, item in enumerate(self._items):
            if item.id == credential.id:
                self._items[index] = credential
                return
        raise KeyError(f"Credential {credential.id} not found")

    def delete(self, credential_id: int) -> None:
        self._items = [item for item in self._items if item.id != credential_id]
