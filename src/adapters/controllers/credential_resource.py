"""
Adapter : Controller Falcon pour la ressource /credentials.

Rôle strict : lire la requête HTTP, appeler le use case, formater
la réponse. Aucune logique métier ici.
"""

import json

import falcon

from src.adapters.presenters.credential_presenter import CredentialPresenter
from src.application.use_cases.create_credential import (
    CreateCredentialInput,
    CreateCredentialUseCase,
)
from src.application.use_cases.delete_credential import (
    DeleteCredentialInput,
    DeleteCredentialUseCase,
)
from src.application.use_cases.list_credentials import ListCredentialsUseCase
from src.domain.exceptions.credential_exceptions import InvalidCredentialError


class CredentialListResource:

    def __init__(
        self,
        create_use_case: CreateCredentialUseCase,
        list_use_case: ListCredentialsUseCase,
    ):
        self._create_use_case = create_use_case
        self._list_use_case = list_use_case

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        items = self._list_use_case.execute()
        resp.media = CredentialPresenter.present_list(items)
        resp.status = falcon.HTTP_200

    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        body = json.loads(req.bounded_stream.read())
        try:
            input_data = CreateCredentialInput(
                service=body.get("service"),
                username=body.get("username"),
                password=body.get("password"),
            )
            output = self._create_use_case.execute(input_data)
            resp.media = CredentialPresenter.present_created(output)
            resp.status = falcon.HTTP_201
        except InvalidCredentialError as e:
            resp.media = {"error": str(e)}
            resp.status = falcon.HTTP_400


class CredentialDetailResource:

    def __init__(self, delete_use_case: DeleteCredentialUseCase):
        self._delete_use_case = delete_use_case

    def on_delete(self, req: falcon.Request, resp: falcon.Response, credential_id: int) -> None:
        try:
            self._delete_use_case.execute(DeleteCredentialInput(credential_id=int(credential_id)))
            resp.status = falcon.HTTP_204
        except InvalidCredentialError as e:
            resp.media = {"error": str(e)}
            resp.status = falcon.HTTP_404
