from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository[Task]):

    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)

    async def get_by_id_for_user(
        self,
        task_id: int,
        user_id: int,
    ) -> Task | None:
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id,
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_all_for_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Task]:
        statement = (
            select(Task)
            .where(Task.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def count_for_user(self, user_id: int) -> int:
        statement = (
            select(func.count())
            .select_from(Task)
            .where(Task.user_id == user_id)
        )

        result = await self.session.execute(statement)

        return result.scalar_one()