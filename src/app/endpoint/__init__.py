from fastapi import APIRouter
from . import auth, profile

router = APIRouter()
router.include_router(auth.router, prefix="/auth")
router.include_router(profile.router)