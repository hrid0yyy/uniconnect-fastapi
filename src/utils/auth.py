from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import os

class APIKeyAuth:
    def __init__(self, server_key: str):
        self.server_key = server_key
        self.algorithm = "HS256"

    def verify_token(self, token: str) -> bool:
        try:
            payload = jwt.decode(
                token,
                self.server_key,
                algorithms=[self.algorithm]
            )
            if payload.get("source") != "spring-boot-server":
                return False
            return True
        except JWTError:
            return False