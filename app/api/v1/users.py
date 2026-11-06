from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.models.user import User
from app.api.dependencies import (
    CurrentUser,
    UserServiceDep,
    require_roles,
)
from app.schemas.auth import UserResponse
from app.schemas.user import (
    UserUpdate,
    ChangePasswordRequest,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: CurrentUser,
):
    return current_user


@router.patch(
    "/me",
    response_model=UserResponse,
)
async def update_me(
    data: UserUpdate,
    current_user: CurrentUser,
    user_service: UserServiceDep,
):
    return await user_service.update_profile(
        current_user,
        data,
    )


@router.post(
    "/me/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def change_password(
    data: ChangePasswordRequest,
    current_user: CurrentUser,
    user_service: UserServiceDep,
):
    await user_service.change_password(
        current_user,
        data,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/admin",
    response_model=UserResponse,
)
async def admin_only(
    current_user: Annotated[
        User,
        Depends(require_roles("ADMIN")),
    ],
):
    return current_user