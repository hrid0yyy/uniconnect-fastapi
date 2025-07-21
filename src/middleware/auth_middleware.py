from fastapi import Request, HTTPException
from ..utils.auth import APIKeyAuth
import os

auth_handler = APIKeyAuth(os.getenv("SERVER_SECRET_KEY"))

async def verify_server_token(request: Request, call_next):
    # Skip auth for swagger docs
    if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)

    token = request.headers.get("X-Server-Token")
    if not token:
        raise HTTPException(
            status_code=401,
            detail="No server token provided"
        )

    if not auth_handler.verify_token(token):
        raise HTTPException(
            status_code=403,
            detail="Invalid server token"
        )

    return await call_next(request)