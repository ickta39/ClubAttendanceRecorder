from typing import Annotated

from model.response import ProfileResponse
from auth.token import verify_user
import db

from fastapi import APIRouter, Depends

from db.model import Profile, User


router = APIRouter()

@router.get("/profile")
async def get_profile(session: db.session_deps, id: Annotated[int, Depends(verify_user)]):
    user = session.get(User, id)
    profile = session.get(Profile, id)

    return ProfileResponse(id=id, name=profile.name, admin=user.admin)