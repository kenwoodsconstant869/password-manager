from src.application.interfaces.user_repository import UserRepository
from src.domain.entities.user import User


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._user: User | None = None

    def save(self, user: User) -> User:
        self._user = user
        return user

    def get_the_user(self) -> User | None:
        return self._user
