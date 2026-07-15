"""
Frameworks & Drivers : point d'entrée Falcon.
"""

import os

import falcon

from src.adapters.controllers.credential_resource import (
    CredentialDetailResource,
    CredentialListResource,
)
from src.adapters.repositories.sqlite_credential_repository import (
    SQLiteCredentialRepository,
)
from src.adapters.repositories.sqlite_user_repository import SQLiteUserRepository
from src.application.use_cases.create_credential import CreateCredentialUseCase
from src.application.use_cases.delete_credential import DeleteCredentialUseCase
from src.application.use_cases.list_credentials import ListCredentialsUseCase
from src.infrastructure.db.connection import get_connection
from src.infrastructure.security.fernet_encryption_service import (
    FernetEncryptionService,
)


def create_app() -> falcon.App:
    connection = get_connection()

    encryption_key = os.environ.get("ENCRYPTION_KEY")
    if not encryption_key:
        raise RuntimeError(
            "La variable d'environnement ENCRYPTION_KEY est requise "
            "(générez-la avec FernetEncryptionService.generate_key())."
        )
    encryption = FernetEncryptionService(key=encryption_key.encode())

    credential_repository = SQLiteCredentialRepository(connection)
    user_repository = SQLiteUserRepository(connection)

    create_credential_use_case = CreateCredentialUseCase(credential_repository, encryption)
    list_credentials_use_case = ListCredentialsUseCase(credential_repository, encryption)
    delete_credential_use_case = DeleteCredentialUseCase(credential_repository)

    app = falcon.App()
    app.add_route(
        "/credentials",
        CredentialListResource(create_credential_use_case, list_credentials_use_case),
    )
    app.add_route(
        "/credentials/{credential_id}",
        CredentialDetailResource(delete_credential_use_case),
    )
    return app


app = create_app()