from flask import Flask, Request

from admin_api.exceptions import TokenNotProvided
from admin_api.integrations.flask.token_parser import TokenParserBase

from ...sdk.auth_manager import AdminApiAuth

FLASK_EXTENSION_NAME = "admin_api"


class AdminApiFlask(AdminApiAuth):
    def __init__(self, token_parser: TokenParserBase, timeout_ms=300):
        super().__init__(timeout_ms)
        self.token_parser: TokenParserBase = token_parser

    def init_app(self, app: Flask) -> None:
        app.extensions[FLASK_EXTENSION_NAME] = self

    def parse_token(self, request: Request) -> str:
        token = self.token_parser.get_token(request)
        if not token:
            raise TokenNotProvided
        return token
