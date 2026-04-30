from enum import Enum
import sqlite3
from typing import Annotated, Any

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
import jwt
import os

from datetime import datetime, timezone, timedelta

from sqlmodel import Session

import db
from db.model import User

class VerifyResult(Enum):
    SUCCESS = 0
    EXPIRED = -1
    NOT_FOUND = -2
    ERROR = -3

def generate_token(user_id: int):
    now = datetime.now(tz=timezone.utc)

    payload = {
        "exp": now + timedelta(days=7),
        "iat": now,
        "sub": str(user_id),
        "user-id": user_id
    }

    return jwt.encode(payload, os.getenv("SESSION_SECRET"), algorithm="HS256")

def verify_token(token, session: Session) -> tuple[VerifyResult, dict[str, Any]]:
    try:
        decoded = jwt.decode(token, os.getenv("SESSION_SECRET"), algorithms=["HS256"])

        user = session.get(User, decoded["user-id"])

        if not user:
            return (VerifyResult.NOT_FOUND, decoded)

        return (
                VerifyResult.SUCCESS,
                decoded
            )
    except jwt.ExpiredSignatureError:
        return (VerifyResult.EXPIRED, None)

def verify_user(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))], session: db.session_deps) -> int:
    result = verify_token(token, session)

    if (result[0] != VerifyResult.SUCCESS):
        raise HTTPException(401)

    return result[1]["user-id"]