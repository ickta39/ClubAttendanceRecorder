from typing import Annotated

from auth.token import verify_user
import db

from fastapi import APIRouter, Depends

from db.model import Profile


router = APIRouter()

@router.get("/profile")
async def get_profile(session: db.session_deps, id: Annotated[int, Depends(verify_user)]):
    return id