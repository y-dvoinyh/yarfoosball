from abc import ABC, abstractmethod
from typing import Type

from src.config.database.db_halper import db_helper
from src.orx.player.repository import PlayersRepository
from src.orx.league.repository import LeaguesRepository
from src.orx.tournament.repository import TournamentsRepository, TournamentTeamsRepository
from src.orx.competition.repository import CompetitionsRepository
from src.orx.team.repository import TeamsRepository
from src.orx.match.repository import MatchsRepository, SetRepository
from src.orx.rating.repository import RatingRepository, RatingHistoryRepository


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
        self.tournaments = TournamentsRepository(self.session)
        self.tournament_teams = TournamentTeamsRepository(self.session)
        self.competitions = CompetitionsRepository(self.session)
        self.teams = TeamsRepository(self.session)
        self.matches = MatchsRepository(self.session)
        self.sets = SetRepository(self.session)
        self.ratings = RatingRepository(self.session)
        self.rating_history = RatingHistoryRepository(self.session)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
