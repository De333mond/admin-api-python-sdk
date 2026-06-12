from flask import Flask

from ...sdk.auth_manager import AdminApiAuth

FLASK_EXTENSION_NAME = "admin_api"


class AdminApiFlask(AdminApiAuth):
    def init_app(self, app: Flask) -> None:
        app.extensions[FLASK_EXTENSION_NAME] = self
