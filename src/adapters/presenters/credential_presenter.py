"""
Adapter : présente les résultats des use cases sous une forme adaptée à l'API
(dict JSON-sérialisable). Isole la structure HTTP du reste de l'app.
"""

from src.application.use_cases.create_credential import CreateCredentialOutput
from src.application.use_cases.list_credentials import CredentialListItem


class CredentialPresenter:

    @staticmethod
    def present_created(output: CreateCredentialOutput) -> dict:
        return {"id": output.id, "service": output.service, "username": output.username}

    @staticmethod
    def present_list(items: list[CredentialListItem]) -> list[dict]:
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
