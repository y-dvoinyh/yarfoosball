from typing import Type, Optional, Generic, Sequence
from abc import ABC, abstractmethod

from sqlalchemy import delete, select, update, text
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

    async def update_or_create(self, data: UpdateSchemaType or PartialSchemaType, **filters) -> ModelType:
        data = data.model_dump()
        instance = await self._session.execute(select(self.model).filter_by(**filters))
        instance = instance .scalar_one_or_none()
        if instance:
            for key, value in data.items():
                if value is not None:
                    setattr(instance, key, value)
        else:
            instance = self.model(**data)
            self._session.add(instance)
        await self._session.flush()
        await self._session.refresh(instance)
        return instance

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
            **filters
    ) -> Sequence[ModelType]:
        stmt = select(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)

        stmt = stmt.order_by(text(order))\
            .limit(limit)\
            .offset(offset)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def all(self, order = "id") -> Sequence[ModelType]:
        stmt = select(self.model).order_by(text(order))
        result = await self._session.execute(stmt)
        return result.scalars().all()