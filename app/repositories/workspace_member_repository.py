from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.models.workspace_member import WorkspaceMember, WorkspaceRole


class WorkspaceMemberRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        workspace_id: int,
        user_id: int,
        role: str,
    ) -> WorkspaceMember:
        member = WorkspaceMember(
            workspace_id=workspace_id,
            user_id=user_id,
            role=role,
        )

        self.session.add(member)
        await self.session.flush()
        await self.session.refresh(member)

        return member

    async def get_by_workspace_and_user(
        self,
        workspace_id: int,
        user_id: int,
    ) -> WorkspaceMember | None:
        statement = select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
        )

        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_all_by_workspace(
        self,
        workspace_id: int,
    ) -> list[WorkspaceMember]:
        statement = (
            select(WorkspaceMember)
            .where(WorkspaceMember.workspace_id == workspace_id)
            .order_by(WorkspaceMember.created_at.asc())
        )

        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def delete(
        self,
        member: WorkspaceMember,
    ) -> None:
        await self.session.delete(member)
        await self.session.flush()

    async def count_owners(self, workspace_id: int) -> int:
        statement = (
            select(func.count(WorkspaceMember.id))
            .where(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.role == WorkspaceRole.OWNER.value,
            )
        )

        result = await self.session.execute(statement)
        return result.scalar_one()