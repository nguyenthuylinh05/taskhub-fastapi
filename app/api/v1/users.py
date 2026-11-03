from fastapi import APIRouter

from app.api.dependencies import CurrentUser
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