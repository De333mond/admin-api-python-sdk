import pytest


@pytest.mark.parametrize(
    "path",
    [
        "admin_api",
        "admin_api.integrations.flask",
        "admin_api.sdk.auth_manager",
        "admin_api.sdk.auth_context",
        "admin_api.api",
        "admin_api.api.users",
        "admin_api.api.mplk",
    ],
)
def test_import(path):
    module = __import__(path)
    assert module is not None
