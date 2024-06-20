from typing import Optional, List, Any
from datetime import datetime, date
from pydantic import BaseModel, Field, Json


from src.orx.tournament.schemas import BaseTournament
from src.orx.competition.schemas import CreateCompetition


class BaseScheme(BaseModel):
    id: str = Field(..., alias='_id')
    name: Optional[str] = None


class Team(BaseScheme):
    players: Optional[List[str]]


class Player(BaseScheme):
    ...


class MatchTeam(BaseScheme):
    players: List[str]


class MatchSet(BaseScheme):
    score: List[int]


class Match(BaseScheme):
    first_team: MatchTeam
    second_team: MatchTeam
    sets: List[MatchSet]


class Competition(BaseScheme):
    start_datetime: datetime
    ferst_team: str
    second_team: str
    table_name: Optional[str] = None
    video_lincs: Optional[List[str]] = None
    matches: List[Match]

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=None).isoformat()
        }


class TeamTournament(BaseScheme):
    date_start: date
    date_end: date
    players: List[Player]
    teams: List[Team]
    competitions: List[Competition]


class BaseTeamTournament(BaseTournament):
    json_data: TeamTournament


class CreateTeamTournament(BaseTeamTournament):
    json_data: Json[Any]


class ResponseTeamTournament(BaseTeamTournament):
    id: int


class CreateTeamCompetition(CreateCompetition):
    json_data: Optional[Json[Any]] = None
