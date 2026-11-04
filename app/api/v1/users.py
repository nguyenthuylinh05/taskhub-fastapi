from fastapi import APIRouter, Depends
from typing import Annotated

from app.models.user import User
from app.api.dependencies import CurrentUser, require_roles
from app.schemas.auth import UserResponse


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