from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
    ) -> RefreshToken:

        token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        self.session.add(token)
        await self.session.commit()
        await self.session.refresh(token)

        return token

    async def get_by_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:

        statement = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def rotate(
        self,
        token_id: int,
        user_id: int,
        new_token_hash: str,
        expires_at: datetime,
        now: datetime,
    ) -> bool:

        # Atomically consume the old token.
        statement = (
            update(RefreshToken)
            .where(
                RefreshToken.id == token_id,
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
                RefreshToken.expires_at > now,
            )
            .values(revoked_at=now)
        )

        result = await self.session.execute(statement)

        if result.rowcount != 1:
            await self.session.rollback()
            return False

        new_token = RefreshToken(
            user_id=user_id,
            token_hash=new_token_hash,
            expires_at=expires_at,
        )

        self.session.add(new_token)

        await self.session.commit()

        return True

    async def revoke_by_hash(
        self,
        token_hash: str,
        now: datetime,
    ) -> None:

        statement = (
            update(RefreshToken)
            .where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked_at.is_(None),
            )
            .values(revoked_at=now)
        )

        await self.session.execute(statement)
        await self.session.commit()


    async def revoke_all_for_user(
        self,
        user_id: int,
        now: datetime,
    ) -> int:
        """Revoke all active refresh tokens belonging to a user."""

        statement = (
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
            )
            .values(revoked_at=now)
        )

        result = await self.session.execute(statement)
        await self.session.commit()

        return result.rowcount or 0
