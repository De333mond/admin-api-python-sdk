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
