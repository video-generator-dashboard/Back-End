from .endpoints import auth
from .endpoints import video
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix='/api/v1/auth',
    tags=['Auth']
)

api_router.include_router(
    video.router,
    prefix='/api/v1/video',
    tags=['Video']
)