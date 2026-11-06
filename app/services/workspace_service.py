from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.roles import GlobalRole, WorkspaceRole
from app.models.user import User
from app.models.workspace import Workspace
from app.repositories.workspace_repository import WorkspaceRepository
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.repositories.user_repository import UserRepository

class WorkspaceService:
    def __init__(
        self,
        session: AsyncSession,
        workspace_repository: WorkspaceRepository,
        member_repository: WorkspaceMemberRepository,
        user_repository: UserRepository,
    ):
        self.session = session
        self.workspace_repository = workspace_repository
        self.member_repository = member_repository
        self.user_repository = user_repository

    async def create_workspace(
        self,
        name: str,
        current_user: User,
    ) -> Workspace:
        try:
            workspace = await self.workspace_repository.create(
                name=name,
                owner_id=current_user.id,
            )

            await self.member_repository.create(
                workspace_id=workspace.id,
                user_id=current_user.id,
                role=WorkspaceRole.OWNER.value,
            )

            await self.session.commit()
            await self.session.refresh(workspace)

            return workspace

        except Exception:
            await self.session.rollback()
            raise

    async def list_my_workspaces(
        self,
        current_user: User,
    ) -> list[Workspace]:
        return await self.workspace_repository.get_all_for_user(
            user_id=current_user.id,
        )

    async def get_workspace(
        self,
        workspace_id: int,
        current_user: User,
    ) -> Workspace:
        # ADMIN có quyền truy cập toàn hệ thống.
        if current_user.role == GlobalRole.ADMIN.value:
            workspace = await self.workspace_repository.get_by_id(
                workspace_id,
            )
        else:
            workspace = await self.workspace_repository.get_by_id_for_user(
                workspace_id=workspace_id,
                user_id=current_user.id,
            )

        if workspace is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found",
            )

        return workspace

    async def delete_workspace(
        self,
        workspace_id: int,
        current_user: User,
    ) -> None:
        workspace = await self.workspace_repository.get_by_id(
            workspace_id,
        )

        if workspace is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found",
            )

        # ADMIN có quyền quản trị toàn hệ thống.
        if current_user.role != GlobalRole.ADMIN.value:
            membership = (
                await self.member_repository.get_by_workspace_and_user(
                    workspace_id=workspace_id,
                    user_id=current_user.id,
                )
            )

            if (
                membership is None
                or membership.role != WorkspaceRole.OWNER.value
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only workspace owners can delete this workspace",
                )

        try:
            await self.workspace_repository.delete(workspace)
            await self.session.commit()

        except Exception:
            await self.session.rollback()
            raise


    async def _require_workspace_owner(
        self,
        workspace_id: int,
        current_user: User,
    ) -> Workspace:
        workspace = await self.get_workspace(
            workspace_id=workspace_id,
            current_user=current_user,
        )

        if current_user.role == GlobalRole.ADMIN.value:
            return workspace

        membership = await self.member_repository.get_by_workspace_and_user(
            workspace_id=workspace_id,
            user_id=current_user.id,
        )

        if (
            membership is None
            or membership.role != WorkspaceRole.OWNER.value
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only workspace owners can manage members",
            )

        return workspace

    async def list_members(
        self,
        workspace_id: int,
        current_user: User,
    ):
        await self.get_workspace(
            workspace_id=workspace_id,
            current_user=current_user,
        )

        return await self.member_repository.get_all_by_workspace(
            workspace_id=workspace_id,
        )

    async def add_member(
        self,
        workspace_id: int,
        email: str,
        role: WorkspaceRole,
        current_user: User,
    ):
        await self._require_workspace_owner(
            workspace_id=workspace_id,
            current_user=current_user,
        )

        user = await self.user_repository.get_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        existing_member = (
            await self.member_repository.get_by_workspace_and_user(
                workspace_id=workspace_id,
                user_id=user.id,
            )
        )

        if existing_member is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already a workspace member",
            )

        try:
            member = await self.member_repository.create(
                workspace_id=workspace_id,
                user_id=user.id,
                role=role.value,
            )

            await self.session.commit()
            await self.session.refresh(member)

            return member

        except Exception:
            await self.session.rollback()
            raise

    async def update_member_role(
        self,
        workspace_id: int,
        user_id: int,
        new_role: WorkspaceRole,
        current_user: User,
    ):
        workspace = await self._require_workspace_owner(
            workspace_id=workspace_id,
            current_user=current_user,
        )

        member = await self.member_repository.get_by_workspace_and_user(
            workspace_id=workspace_id,
            user_id=user_id,
        )

        if member is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace member not found",
            )

        if member.role == new_role.value:
            return member

        if (
            user_id == workspace.owner_id
            and new_role != WorkspaceRole.OWNER
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot change the primary owner's role",
            )

        if (
            member.role == WorkspaceRole.OWNER.value
            and new_role != WorkspaceRole.OWNER
        ):
            owner_count = await self.member_repository.count_owners(
                workspace_id=workspace_id,
            )

            if owner_count <= 1:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Workspace must have at least one owner",
                )

        try:
            member.role = new_role.value

            await self.session.commit()
            await self.session.refresh(member)

            return member

        except Exception:
            await self.session.rollback()
            raise

    async def remove_member(
        self,
        workspace_id: int,
        user_id: int,
        current_user: User,
    ) -> None:
        workspace = await self._require_workspace_owner(
            workspace_id=workspace_id,
            current_user=current_user,
        )

        member = await self.member_repository.get_by_workspace_and_user(
            workspace_id=workspace_id,
            user_id=user_id,
        )

        if member is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace member not found",
            )

        if user_id == workspace.owner_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot remove the primary workspace owner",
            )

        if member.role == WorkspaceRole.OWNER.value:
            owner_count = await self.member_repository.count_owners(
                workspace_id=workspace_id,
            )

            if owner_count <= 1:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Workspace must have at least one owner",
                )

        try:
            await self.member_repository.delete(member)
            await self.session.commit()

        except Exception:
            await self.session.rollback()
            raise