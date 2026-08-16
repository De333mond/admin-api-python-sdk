from flask import Flask, Request

from admin_api.api.client import SyncApi
from admin_api.exceptions import TokenNotProvided
from admin_api.integrations.flask.token_parser import TokenParserBase
from admin_api.sdk.auth_manager import AdminApiAuth

FLASK_EXTENSION_NAME = "admin_api"


class AdminApiFlask(AdminApiAuth):
    def __init__(
        self,
        token_parser: TokenParserBase,
        api: SyncApi | None = None,
        *,
        base_url: str | None = None,
        timeout_ms: int = 300,
        service_name: str | None = None,
    ) -> None:
        super().__init__(
            api,
            base_url=base_url,
            timeout_ms=timeout_ms,
            service_name=service_name,
        )
        self.token_parser: TokenParserBase = token_parser

    def init_app(self, app: Flask) -> None:
        app.extensions[FLASK_EXTENSION_NAME] = self

    def parse_token(self, request: Request) -> str:
        token = self.token_parser.get_token(request)
        if not token:
            raise TokenNotProvided
        return token
