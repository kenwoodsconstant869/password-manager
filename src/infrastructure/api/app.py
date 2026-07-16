"""
Frameworks & Drivers : point d'entrée Falcon.
"""

import os

import falcon

from src.adapters.controllers.auth_resources import (
    CredentialDetailResource,
    CredentialListResource,
    LoginResource,
    RegisterUserResource,
)
from src.adapters.repositories.sqlite_credential_repository import (
    SQLiteCredentialRepository,
)
from src.adapters.repositories.sqlite_user_repository import SQLiteUserRepository
from src.application.use_cases.authenticate_user import (
    AuthenticateUserInput,
    AuthenticateUserUseCase,
)
from src.application.use_cases.create_credential import CreateCredentialUseCase
from src.application.use_cases.delete_credential import DeleteCredentialUseCase
from src.application.use_cases.list_credentials import ListCredentialsUseCase
from src.application.use_cases.register_user import RegisterUserUseCase
from src.domain.exceptions.user_exceptions import AuthenticationError, InvalidUserError
from src.infrastructure.db.connection import get_connection
from src.infrastructure.security.fernet_encryption_service import (
    FernetEncryptionService,
)


class MasterPasswordMiddleware:
    def __init__(self, auth_use_case: AuthenticateUserUseCase):
        self._auth_use_case = auth_use_case

    def process_request(self, req: falcon.Request, resp: falcon.Response) -> None:
        if req.path.lower() in {"/register", "/login", "/health"}:
            return

        master_password = req.get_header("X-Master-Password")
        if not master_password:
            raise falcon.HTTPUnauthorized(
                title="Authentication required",
                description="Provide the X-Master-Password header.",
            )

        try:
            self._auth_use_case.execute(
                AuthenticateUserInput(master_password=master_password)
            )
        except InvalidUserError as exc:
            raise falcon.HTTPUnauthorized(
                title="Authentication required",
                description=str(exc),
            ) from exc
        except AuthenticationError as exc:
            raise falcon.HTTPUnauthorized(
                title="Authentication required",
                description=str(exc),
            ) from exc


def create_app() -> falcon.App:
    connection = get_connection(os.environ.get("PASSWORD_MANAGER_DB_PATH"))

    encryption_key = os.environ.get("ENCRYPTION_KEY")
    if encryption_key:
        key_bytes = encryption_key.encode()
    else:
        key_bytes = FernetEncryptionService.load_or_create_key(
            os.environ.get("PASSWORD_MANAGER_KEY_PATH")
        )
    encryption = FernetEncryptionService(key=key_bytes)

    credential_repository = SQLiteCredentialRepository(connection)
    user_repository = SQLiteUserRepository(connection)

    create_credential_use_case = CreateCredentialUseCase(credential_repository, encryption)
    list_credentials_use_case = ListCredentialsUseCase(credential_repository, encryption)
    delete_credential_use_case = DeleteCredentialUseCase(credential_repository)
    register_user_use_case = RegisterUserUseCase(user_repository)
    authenticate_user_use_case = AuthenticateUserUseCase(user_repository)

    app = falcon.App(middleware=[MasterPasswordMiddleware(authenticate_user_use_case)])
    app.add_route("/register", RegisterUserResource(register_user_use_case))
    app.add_route("/login", LoginResource(authenticate_user_use_case))
    app.add_route(
        "/credentials",
        CredentialListResource(create_credential_use_case, list_credentials_use_case),
    )
    app.add_route(
        "/credentials/{credential_id}",
        CredentialDetailResource(delete_credential_use_case),
    )
    return app


def close_app_connections() -> None:
    if "app" in globals():
        try:
            import sqlite3

            for connection in getattr(app, "_connections", []):
                if isinstance(connection, sqlite3.Connection):
                    connection.close()
        except Exception:
            pass


app = create_app()