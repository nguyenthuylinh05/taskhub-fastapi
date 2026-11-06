
from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        model: type[ModelType],
        session: AsyncSession,
    ):
        self.model = model
        self.session = session

    async def create(self, data: dict[str, Any]) -> ModelType:
        obj = self.model(**data)

        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)

        return obj

    async def get_by_id(self, obj_id: int) -> ModelType | None:
        return await self.session.get(self.model, obj_id)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
    ) -> list[ModelType]:

        statement = (
            select(self.model)
            .offset(skip)
            .limit(limit)
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def update(
        self,
        obj: ModelType,
        data: dict[str, Any],
    ) -> ModelType:

        for key, value in data.items():
            setattr(obj, key, value)

        await self.session.commit()
        await self.session.refresh(obj)

        return obj

    async def delete(self, obj: ModelType) -> None:
        await self.session.delete(obj)
        await self.session.commit()

    async def count(self) -> int:
        from sqlalchemy import func

        statement = select(func.count()).select_from(self.model)

        result = await self.session.execute(statement)

        return result.scalar_one()
