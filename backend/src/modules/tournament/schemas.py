from typing import Optional
from pydantic import BaseModel

from src.models.enums import TournamentType


class BaseTournament(BaseModel):
    name: str
    description: str
    type: TournamentType
    league_id: int


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
