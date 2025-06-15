from fastapi import APIRouter

from main.modules.auth import router as auth_router
from main.modules.user import router as user_router
from main.modules.router import router as router_router
from main.modules.subscriber import router as subscriber_router

api_router = APIRouter()

api_router.include_router(
    auth_router.router,
    prefix="/auth",
    tags=["Authentication Module"]
)

api_router.include_router(
    user_router.router,
    prefix="/user",
    tags=["User Module"]
)

api_router.include_router(
    router_router.router,
    prefix="/router",
    tags=["Router Module"]
)

api_router.include_router(
    subscriber_router.router,
    prefix="/subscriber",
    tags=["Subscriber Module"]
)