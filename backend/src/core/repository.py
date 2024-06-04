from typing import Type, Optional, Generic, Sequence
from abc import ABC, abstractmethod

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .types import ModelType, CreateSchemaType, UpdateSchemaType, PartialSchemaType


class AbstractRepository(ABC):

    @abstractmethod
    async def create(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def list(self, **kwargs):
        raise NotImplementedError


class SqlAlchemyRepository(
    AbstractRepository,
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, PartialSchemaType]
):
    model: Type[ModelType] = None

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, data: CreateSchemaType) -> ModelType:
        instance = self.model(**data.model_dump())

        self._session.add(instance)
        await self._session.flush()
        await self._session.refresh(instance)
        return instance

    async def update(self, data: UpdateSchemaType, **filters) -> ModelType:
        stmt = update(self.model).values(**data).filter_by(**filters).returning(self.model)
        res = await self._session.execute(stmt)
        await self._session.flush()
        return res.scalar_one()

    async def delete(self, **filters) -> None:
        await self._session.execute(delete(self.model).filter_by(**filters))
        await self._session.flush()

    async def get_single(self, **filters) -> Optional[ModelType] | None:
        row = await self._session.execute(select(self.model).filter_by(**filters))
        return row.scalar_one_or_none()

    async def list(
            self,
            order: str = "id",
            limit: int = 100,
            offset: int = 0,
            ** filters
    ) -> Sequence[ModelType]:
        stmt = select(self.model)
        # if filters:
        #     stmt = stmt.filter_by(**filters)

        # stmt = stmt.order_by(*order)\
        #     .limit(limit)\
        #     .offset(offset)
        result = await self._session.execute(stmt)
        return result.scalars().all()