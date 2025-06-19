from fastapi import APIRouter

from main.modules.otp import router as otp_router
from main.modules.auth import router as auth_router
from main.modules.user import router as user_router
from main.modules.router import router as router_router
from main.modules.dashboard import router as dashboard_router

api_router = APIRouter()

api_router.include_router(
    otp_router.router,
    prefix="/otp",
    tags=["OTP Module"]
)

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
    dashboard_router.router,
    prefix="/dashboard",
    tags=["Dashboard Module"]
)