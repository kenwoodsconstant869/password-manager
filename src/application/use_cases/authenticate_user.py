"""Use case: authentifier l'utilisateur unique avec son mot de passe maître."""

from dataclasses import dataclass

from src.application.interfaces.user_repository import UserRepository
from src.domain.exceptions.user_exceptions import AuthenticationError, InvalidUserError


@dataclass
class AuthenticateUserInput:
    master_password: str


class AuthenticateUserUseCase:

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self, input_data: AuthenticateUserInput) -> bool:
        user = self._repository.get_the_user()
        if user is None:
            raise InvalidUserError("Aucun utilisateur configuré. Initialisez d'abord le coffre-fort.")
        return user.verify_password(input_data.master_password)
