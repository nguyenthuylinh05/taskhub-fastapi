from fastapi import HTTPException, status

from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserRegister
from app.core.security import verify_password, create_access_token
from app.schemas.auth import UserLogin

class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

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
        }

        return await self.repository.create(user_data)

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

        access_token = create_access_token(
            subject=str(user.id)
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
