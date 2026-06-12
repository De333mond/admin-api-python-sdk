import grpc

from admin_api.grpc._generated.auth import auth_pb2
from admin_api.grpc._generated.auth.auth_pb2_grpc import AuthServiceStub
from admin_api.grpc.dto.auth import TokenPayload, UserData


class AuthGRPCService:
    def __init__(self, grpc_target: str) -> None:
        self.url = grpc_target
        self.channel: grpc.Channel | None = None
        self.stub: AuthServiceStub | None = None

    def __enter__(self):
        self.channel = grpc.insecure_channel(self.url)
        self.stub = AuthServiceStub(self.channel)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.channel:
            self.channel.close()

    def get_payload(self, jwt: str) -> TokenPayload:
        if not self.channel or not self.stub:
            raise Exception("You can call methods only in context manager!")

        try:
            request = auth_pb2.GetPayloadRequest(token=jwt)
            response = self.stub.GetPayload(request)
            return TokenPayload(
                user_id=response.user_id,
                role=response.role,
                expires_at=response.expires_at,
                service_name=response.service_name,
                permissions=response.permissions,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                raise Exception("Invalid token") from e
            else:
                raise Exception(f"Auth service error: {e.code()}") from e

    def get_user_data(self, jwt: str) -> UserData:
        if not self.channel or not self.stub:
            raise Exception("You can call methods only in context manager!")

        try:
            request = auth_pb2.GetUserRequest(token=jwt)
            response = self.stub.GetUser(request)
            return UserData.from_response(response)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                raise Exception("Invalid token") from e
            else:
                raise Exception(f"Auth service error: {e.code()}") from e

    def check_conn(self) -> bool:
        if not self.channel:
            raise Exception("You can call methods only in context manager!")

        try:
            grpc.channel_ready_future(self.channel).result(timeout=15)
            return True
        except grpc.FutureTimeoutError:
            return False
        except AttributeError:
            return False
