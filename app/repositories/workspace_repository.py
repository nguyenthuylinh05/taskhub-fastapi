from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember


class WorkspaceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        name: str,
        owner_id: int,
    ) -> Workspace:
        workspace = Workspace(
            name=name,
            owner_id=owner_id,
        )

        self.session.add(workspace)
        await self.session.flush()
        await self.session.refresh(workspace)

        return workspace

    async def get_by_id(
        self,
        workspace_id: int,
    ) -> Workspace | None:
        statement = select(Workspace).where(
            Workspace.id == workspace_id
        )

        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_id_for_user(
        self,
        workspace_id: int,
        user_id: int,
    ) -> Workspace | None:
        statement = (
            select(Workspace)
            .join(
                WorkspaceMember,
                WorkspaceMember.workspace_id == Workspace.id,
            )
            .where(
                Workspace.id == workspace_id,
                WorkspaceMember.user_id == user_id,
            )
        )

        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_all_for_user(
        self,
        user_id: int,
    ) -> list[Workspace]:
        statement = (
            select(Workspace)
            .join(
                WorkspaceMember,
                WorkspaceMember.workspace_id == Workspace.id,
            )
            .where(WorkspaceMember.user_id == user_id)
            .order_by(Workspace.created_at.desc())
        )

        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def delete(
        self,
        workspace: Workspace,
    ) -> None:
        await self.session.delete(workspace)
        await self.session.flush()