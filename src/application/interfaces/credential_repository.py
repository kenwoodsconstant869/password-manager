"""Port (interface abstraite) pour la persistance des Credential."""

from abc import ABC, abstractmethod

from src.domain.entities.credential import Credential


class CredentialRepository(ABC):

    @abstractmethod
    def add(self, credential: Credential) -> Credential:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, credential_id: int) -> Credential | None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Credential]:
        raise NotImplementedError

    @abstractmethod
    def update(self, credential: Credential) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, credential_id: int) -> None:
        raise NotImplementedError
