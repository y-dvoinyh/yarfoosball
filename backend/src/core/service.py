from typing import Generic, Optional
from abc import ABC, abstractmethod

from src.core.uow import UnitOfWork
from src.core.repository import SqlAlchemyRepository

from .types import ModelType, CreateSchemaType, UpdateSchemaType, PartialSchemaType


class AbstractService(ABC):

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


class BaseService(Generic[CreateSchemaType]):
    """Базовый сервис CRUD"""
    repository_name: str = None

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @property
    def repository(self) -> SqlAlchemyRepository:
        return self.uow.rep.get(self.repository_name)

    async def create(self, data: CreateSchemaType):
        result = await self.repository.create(data)
        await self.uow.commit()
        return result

    async def update(self, data: UpdateSchemaType, **filters):
        result = await self.repository.update(data, **filters)
        await self.uow.commit()
        return result

    async def delete(self, **filters) -> None:
        await self.repository.delete(**filters)
        await self.uow.commit()

    async def get_single(self, **filters) -> Optional[ModelType] | None:
        return await self.repository.get_single(**filters)

    async def list(
            self,
            order: str = "id",
            limit: int = 100,
            offset: int = 0,
            **filters
    ):
        return await self.repository.list(order, limit, offset, **filters)
