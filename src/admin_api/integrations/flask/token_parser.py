from flask import Request


class TokenParserBase:
    def get_token(self, request: Request) -> str | None:
        raise NotImplementedError
