from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdate, ChangePasswordRequest


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

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

        # Kiểm tra tài khoản có mật khẩu để xác thực hay không
        if not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is not set for this account",
            )

        # Xác minh mật khẩu hiện tại
        if not verify_password(
            data.current_password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )

        # Không cho phép dùng lại mật khẩu hiện tại
        if verify_password(
            data.new_password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from current password",
            )

        # Hash mật khẩu mới trước khi lưu
        user.hashed_password = hash_password(data.new_password)

        await self.repository.update(
            user,
            {"hashed_password": user.hashed_password},
        )