from fastapi import APIRouter, status

from app.api.dependencies import AuthServiceDep
from app.schemas.auth import UserRegister, UserResponse
from app.schemas.auth import UserLogin, TokenResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: UserRegister,
    service: AuthServiceDep,
):
    return await service.register(data)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    data: UserLogin,
    service: AuthServiceDep,
):
    return await service.login(data)
