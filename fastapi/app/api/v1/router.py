from fastapi import APIRouter

from app.api.v1 import auth, users, videos


router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(videos.router)
