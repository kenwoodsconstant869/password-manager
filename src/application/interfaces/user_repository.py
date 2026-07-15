"""Port (interface abstraite) pour la persistance de l'utilisateur unique."""

from abc import ABC, abstractmethod

from src.domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def save(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_the_user(self) -> User | None:
        raise NotImplementedError
