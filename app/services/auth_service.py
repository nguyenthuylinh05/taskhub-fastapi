from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
)
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.schemas.auth import UserRegister, UserLogin
from app.core.roles import GlobalRole

def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class AuthService:

    def __init__(
        self,
        repository: UserRepository,
        refresh_repository: RefreshTokenRepository,
    ):
        self.repository = repository
        self.refresh_repository = refresh_repository

    async def register(self, data: UserRegister):
        existing_user = await self.repository.get_by_email(
            str(data.email)
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user_data = {
            "email": str(data.email),
            "full_name": data.full_name,
            "hashed_password": hash_password(data.password),
            "role": GlobalRole.MEMBER.value,
    }

        return await self.repository.create(user_data)

    async def _issue_token_pair(self, user_id: int):
        access_token = create_access_token(
            subject=str(user_id)
        )

        refresh_token = create_refresh_token()

        expires_at = utc_now() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

        await self.refresh_repository.create(
            user_id=user_id,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=expires_at,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def login(self, data: UserLogin):
        user = await self.repository.get_by_email(
            str(data.email)
        )

        if user is None or not verify_password(
            data.password,
            user.hashed_password or "",
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )

        return await self._issue_token_pair(user.id)

    async def refresh(self, raw_token: str):
        now = utc_now()

        token_hash = hash_refresh_token(raw_token)

        old_token = await self.refresh_repository.get_by_hash(
            token_hash
        )

        if (
            old_token is None
            or old_token.revoked_at is not None
            or old_token.expires_at <= now
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        user = await self.repository.get_by_id(
            old_token.user_id
        )

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        new_refresh_token = create_refresh_token()

        new_token_hash = hash_refresh_token(
            new_refresh_token
        )

        new_expires_at = now + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

        rotated = await self.refresh_repository.rotate(
            token_id=old_token.id,
            user_id=user.id,
            new_token_hash=new_token_hash,
            expires_at=new_expires_at,
            now=now,
        )

        if not rotated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has already been used",
            )

        new_access_token = create_access_token(
            subject=str(user.id)
        )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }

    async def logout(self, raw_token: str):
        await self.refresh_repository.revoke_by_hash(
            token_hash=hash_refresh_token(raw_token),
            now=utc_now(),
        )
