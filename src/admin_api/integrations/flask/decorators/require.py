import inspect
from functools import wraps

from flask import current_app, request

from admin_api.integrations.flask import FLASK_EXTENSION_NAME, AdminApiFlask
from admin_api.sdk.auth_context import AuthContext


def require(*required: str):
    """Authentication decorator for route handlers.

    Args:
        *required: Variable length argument of permissions.

    This decorator validates the user's authentication token and checks if the user
    has the required permissions to access the endpoint. It also automatically injects
    the AuthContext object into the decorated function's parameters if there is
    a parameter annotated with the AuthContext type.
    """

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                raise Exception("Token not provided")

            auth_manager: AdminApiFlask = current_app.extensions[FLASK_EXTENSION_NAME]
            auth_context = auth_manager.check(required, token)

            sig = inspect.signature(f)
            for param_name, param in sig.parameters.items():
                if param.annotation == AuthContext:
                    kwargs[param_name] = auth_context
                    break

            return f(*args, **kwargs)

        return decorated

    return decorator
