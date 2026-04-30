import json

from fastapi import APIRouter, HTTPException
from sqlalchemy import Select

import db
from auth import password, token
from db.model import User
from model.body import IdentifyBody

router = APIRouter()

@router.post("/login")
async def login(session: db.session_deps, body: IdentifyBody):
    user: User = session.exec(Select(User).where(User.email == body.email)).first()[0]

    if not user:
        raise HTTPException(400, {"error": "User or password is wrong"})

    if not password.verify_password(body.password, user.password):
        raise HTTPException(400, {"error": "User or password is wrong"})

    return {"token": token.generate_token(user.id)}