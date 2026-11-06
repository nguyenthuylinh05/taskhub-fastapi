
from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.schemas.user import UserUpdate, ChangePasswordRequest


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class UserService:

    def __init__(
        self,
        repository: UserRepository,
        refresh_repository: RefreshTokenRepository,
    ):
        self.repository = repository
        self.refresh_repository = refresh_repository

    async def update_profile(
        self,
        user: User,
        data: UserUpdate,
    ) -> User:
        update_data = data.model_dump(exclude_unset=True)

        return await self.repository.update(
            user,
            update_data,
        )

    async def change_password(
        self,
        user: User,
        data: ChangePasswordRequest,
    ) -> None:

        if not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is not set for this account",
            )

        if not verify_password(
            data.current_password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )

        if verify_password(
            data.new_password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from current password",
            )

        user.hashed_password = hash_password(data.new_password)

        await self.repository.update(
            user,
            {"hashed_password": user.hashed_password},
        )

        # Revoke all active refresh tokens after password change.
        await self.refresh_repository.revoke_all_for_user(
            user_id=user.id,
            now=utc_now(),
        )
