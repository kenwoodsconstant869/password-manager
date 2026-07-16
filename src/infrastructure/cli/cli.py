import sys
from typing import List

from src.adapters.repositories.in_memory_credential_repository import InMemoryCredentialRepository
from src.adapters.repositories.in_memory_user_repository import InMemoryUserRepository
from src.application.use_cases.authenticate_user import AuthenticateUserInput, AuthenticateUserUseCase
from src.application.use_cases.create_credential import CreateCredentialInput, CreateCredentialUseCase
from src.application.use_cases.list_credentials import ListCredentialsUseCase
from src.application.use_cases.register_user import RegisterUserInput, RegisterUserUseCase
from src.infrastructure.security.in_memory_encryption_service import InMemoryEncryptionService


class PasswordManagerCLI:
    def __init__(self, db_path: str | None = None, key_path: str | None = None):
        self._user_repository = InMemoryUserRepository()
        self._credential_repository = InMemoryCredentialRepository()
        self._encryption = InMemoryEncryptionService()
        self._create_use_case = CreateCredentialUseCase(self._credential_repository, self._encryption)
        self._list_use_case = ListCredentialsUseCase(self._credential_repository, self._encryption)
        self._register_use_case = RegisterUserUseCase(self._user_repository)
        self._authenticate_use_case = AuthenticateUserUseCase(self._user_repository)

    def dispatch(self, argv: List[str]) -> object:
        if not argv:
            return self._run_interactive_loop()

        command = argv[0]
        if command == "register" and len(argv) >= 3:
            self._register_use_case.execute(
                RegisterUserInput(username=argv[1], master_password=argv[2])
            )
            return "User registered successfully."

        if command == "add" and len(argv) >= 5:
            master_password = argv[4]
            self._authenticate_use_case.execute(
                AuthenticateUserInput(master_password=master_password)
            )
            self._create_use_case.execute(
                CreateCredentialInput(
                    service=argv[1],
                    username=argv[2],
                    password=argv[3],
                )
            )
            return "Credential added successfully."

        if command == "list" and len(argv) >= 2:
            self._authenticate_use_case.execute(
                AuthenticateUserInput(master_password=argv[1])
            )
            items = self._list_use_case.execute()
            return [
                {
                    "id": item.id,
                    "service": item.service,
                    "username": item.username,
                    "password": item.password,
                    "created_at": item.created_at,
                }
                for item in items
            ]

        return self._help()

    def _run_interactive_loop(self) -> str:
        print(self._help())
        while True:
            command = input("Choisissez une action (register/add/list/exit) : ").strip().lower()
            if command == "exit":
                return "Au revoir."
            if command == "register":
                username = input("Nom d'utilisateur : ").strip()
                master_password = input("Mot de passe maître : ").strip()
                self._register_use_case.execute(
                    RegisterUserInput(username=username, master_password=master_password)
                )
                print("Utilisateur enregistré.")
                continue
            if command == "add":
                service = input("Service : ").strip()
                username = input("Nom d'utilisateur : ").strip()
                password = input("Mot de passe : ").strip()
                master_password = input("Mot de passe maître : ").strip()
                self._authenticate_use_case.execute(
                    AuthenticateUserInput(master_password=master_password)
                )
                self._create_use_case.execute(
                    CreateCredentialInput(service=service, username=username, password=password)
                )
                print("Credential ajouté.")
                continue
            if command == "list":
                master_password = input("Mot de passe maître : ").strip()
                self._authenticate_use_case.execute(
                    AuthenticateUserInput(master_password=master_password)
                )
                items = self._list_use_case.execute()
                for item in items:
                    print(item.service, item.username, item.password)
                continue
            print("Commande inconnue.")

    def _help(self) -> str:
        return (
            "Usage:\n"
            "  register <username> <master_password>\n"
            "  add <service> <username> <password> <master_password>\n"
            "  list <master_password>\n"
            "Ou lancez la CLI sans argument pour saisir les informations interactivement."
        )


def main() -> None:
    cli = PasswordManagerCLI()
    result = cli.dispatch(sys.argv[1:])
    if isinstance(result, list):
        for item in result:
            print(item)
    else:
        print(result)


if __name__ == "__main__":
    main()
