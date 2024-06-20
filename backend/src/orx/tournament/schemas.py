from typing import Optional, Any
from pydantic import BaseModel, Json

from src.models import TournamentType


class BaseTournament(BaseModel):
    name: str
    description: str
    type: TournamentType
    league_id: int
    external_id: Optional[str] = None


class ResponseTournament(BaseTournament):
    id: int


class CreateTournament(BaseTournament):
    ...


class UpdateTournament(BaseTournament):
    ...


class PartialTournament(BaseTournament):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[TournamentType] = None
    league_id: Optional[int] = None


class BaseTournamentTeam(BaseModel):
    name: str
    tournament_id: int
    external_id: Optional[str] = None
    players: Optional[Json[Any]]


class ResponseTournamentTeam(BaseTournamentTeam):
    id: int


class CreateTournamentTeam(BaseTournamentTeam):
    ...


class UpdateTournamentTeam(BaseTournamentTeam):
    ...


class PartialTournamentTeam(BaseTournamentTeam):
    name: Optional[str] = None
    tournament_id: Optional[int] = None
    external_id: Optional[str] = None
    players: Optional[Json[Any]] = None
