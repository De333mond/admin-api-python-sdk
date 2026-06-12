import pytest


@pytest.mark.parametrize(
    "path",
    [
        "admin_api",
        "admin_api.integrations.flask",
        "admin_api.sdk.auth_manager",
        "admin_api.sdk.auth_context",
        "admin_api.grpc",
        "admin_api.grpc.dto",
    ],
)
def test_import(path):
    module = __import__(path)
    assert module is not None


def test_flask_application():
    from flask import Flask

    from admin_api.integrations.flask.flask import AdminApiFlask

    app = Flask(__name__)
    admin_api = AdminApiFlask(grpc_target="admin.kd.mospolytech.ru:50051")
    admin_api.init_app(app)

    app.run()
