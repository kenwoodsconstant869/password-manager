import json

import falcon

from src.application.use_cases.authenticate_user import (
    AuthenticateUserInput,
    AuthenticateUserUseCase,
)
from src.application.use_cases.create_credential import (
    CreateCredentialInput,
    CreateCredentialUseCase,
)
from src.application.use_cases.delete_credential import (
    DeleteCredentialInput,
    DeleteCredentialUseCase,
)
from src.application.use_cases.list_credentials import ListCredentialsUseCase
from src.application.use_cases.register_user import RegisterUserInput, RegisterUserUseCase
from src.domain.exceptions.credential_exceptions import InvalidCredentialError
from src.domain.exceptions.user_exceptions import AuthenticationError, InvalidUserError
from src.adapters.presenters.credential_presenter import CredentialPresenter


class RegisterUserResource:
    def __init__(self, register_use_case: RegisterUserUseCase):
        self._register_use_case = register_use_case

    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        try:
            body = self._read_json(req)
            input_data = RegisterUserInput(
                username=body.get("username"),
                master_password=body.get("master_password"),
            )
            self._register_use_case.execute(input_data)
            resp.media = {"message": "User registered successfully"}
            resp.status = falcon.HTTP_201
        except InvalidUserError as exc:
            resp.media = {"error": str(exc)}
            resp.status = falcon.HTTP_400

    @staticmethod
    def _read_json(req: falcon.Request) -> dict:
        raw_body = req.bounded_stream.read()
        if not raw_body:
            return {}
        return json.loads(raw_body.decode())


class LoginResource:
    def __init__(self, auth_use_case: AuthenticateUserUseCase):
        self._auth_use_case = auth_use_case

    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        try:
            body = self._read_json(req)
            input_data = AuthenticateUserInput(master_password=body.get("master_password"))
            self._auth_use_case.execute(input_data)
            resp.media = {"message": "Authentication successful"}
            resp.status = falcon.HTTP_200
        except InvalidUserError as exc:
            resp.media = {"error": str(exc)}
            resp.status = falcon.HTTP_400
        except AuthenticationError as exc:
            resp.media = {"error": str(exc)}
            resp.status = falcon.HTTP_401

    @staticmethod
    def _read_json(req: falcon.Request) -> dict:
        raw_body = req.bounded_stream.read()
        if not raw_body:
            return {}
        return json.loads(raw_body.decode())


class CredentialListResource:
    def __init__(self, create_use_case: CreateCredentialUseCase, list_use_case: ListCredentialsUseCase):
        self._create_use_case = create_use_case
        self._list_use_case = list_use_case

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        items = self._list_use_case.execute()
        resp.media = CredentialPresenter.present_list(items)
        resp.status = falcon.HTTP_200

    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        try:
            body = self._read_json(req)
            input_data = CreateCredentialInput(
                service=body.get("service"),
                username=body.get("username"),
                password=body.get("password"),
            )
            output = self._create_use_case.execute(input_data)
            resp.media = CredentialPresenter.present_created(output)
            resp.status = falcon.HTTP_201
        except InvalidCredentialError as exc:
            resp.media = {"error": str(exc)}
            resp.status = falcon.HTTP_400

    @staticmethod
    def _read_json(req: falcon.Request) -> dict:
        raw_body = req.bounded_stream.read()
        if not raw_body:
            return {}
        return json.loads(raw_body.decode())


class CredentialDetailResource:
    def __init__(self, delete_use_case: DeleteCredentialUseCase):
        self._delete_use_case = delete_use_case

    def on_delete(self, req: falcon.Request, resp: falcon.Response, credential_id: int) -> None:
        try:
            self._delete_use_case.execute(DeleteCredentialInput(credential_id=int(credential_id)))
            resp.status = falcon.HTTP_204
        except InvalidCredentialError as exc:
            resp.media = {"error": str(exc)}
            resp.status = falcon.HTTP_404
