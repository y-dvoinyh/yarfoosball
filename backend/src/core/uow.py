from abc import ABC, abstractmethod
from typing import Type

from src.config.database.db_halper import db_helper
from src.modules.player.repository import PlayersRepository
from src.modules.league.repository import LeaguesRepository


class IUnitOfWork(ABC):
    players: Type[PlayersRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    players: PlayersRepository = None

    def __init__(self):
        self.session = db_helper.session_factory()
        self.players = PlayersRepository(self.session)
        self.leagues = LeaguesRepository(self.session)
        self.rep = {
            'player': self.players,
            'league': self.leagues
        }

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
