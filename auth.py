import grpc
from typing import Optional
import auth_pb2
import auth_pb2_grpc
from conf import settings

class AuthStub:
    def __init__(self):
        self.channel = grpc.aio.insecure_channel(f"{settings.AUTH_SERVICE_GRPC}")
        self.stub = auth_pb2_grpc.AuthServiceStub(self.channel)

async def decode_access_token(token: str) -> bool:
    """Verify regular user token"""
    async with grpc.aio.insecure_channel(f"{settings.AUTH_SERVICE_GRPC}") as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)
        response = await stub.AuthUser(
            auth_pb2.Token(
                user_type=0,
                session_id=token
            )
        )
        return {"valid": response.code == 200,"detail":response.detail}

async def decode_access_token_admin(token: str) -> bool:
    """Verify admin token"""
    async with grpc.aio.insecure_channel(f"{settings.AUTH_SERVICE_GRPC}") as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)
        response = await stub.AuthUser(
            auth_pb2.Token(
                user_type=1,
                session_id=token
            )
        )
        return {"valid": response.code == 200,"detail":response.detail}

async def decode_access_token_backend_admin(token: str) -> bool:
    """Verify backend admin token"""
    async with grpc.aio.insecure_channel(f"{settings.AUTH_SERVICE_GRPC}") as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)
        response = await stub.AuthUser(
            auth_pb2.Token(
                user_type=2,
                session_id=token
            )
        )
        return {"valid": response.code == 200,"detail":response.detail}