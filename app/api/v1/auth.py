from fastapi import APIRouter, Response, status

from app.api.dependencies import AuthServiceDep
from app.schemas.auth import (
    UserRegister,
    UserResponse,
    UserLogin,
    TokenResponse,
    RefreshTokenRequest,
)


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


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def refresh(
    data: RefreshTokenRequest,
    service: AuthServiceDep,
):
    return await service.refresh(data.refresh_token)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    data: RefreshTokenRequest,
    service: AuthServiceDep,
):
    await service.logout(data.refresh_token)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
