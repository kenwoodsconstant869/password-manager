"""Use case: initialiser le coffre-fort avec un utilisateur et un mot de passe maître."""

from dataclasses import dataclass

from src.application.interfaces.user_repository import UserRepository
from src.domain.entities.user import User
from src.domain.exceptions.user_exceptions import InvalidUserError


@dataclass
class RegisterUserInput:
    username: str
    master_password: str


class RegisterUserUseCase:

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self, input_data: RegisterUserInput) -> None:
        if self._repository.get_the_user() is not None:
            raise InvalidUserError("Le coffre-fort est déjà initialisé.")
        user = User.create(username=input_data.username, master_password=input_data.master_password)
        self._repository.save(user)
