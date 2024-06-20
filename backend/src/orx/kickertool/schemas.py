from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, Field, Json

from src.orx.competition.schemas import BaseCompetition, CreateCompetition, ResponseCompetition


class Stats(BaseModel):
    """Статистика игрока в квалификации"""
    place: int


class BaseScheme(BaseModel):
    id: str = Field(..., alias='_id')
    name: Optional[str] = None


class Player(BaseScheme):
    """Игрок"""
    ...


class Standings(Player):
    """Турнирная таблица"""
    stats: Stats


class Team(BaseScheme):
    """Команда"""
    players: List[Player]


class Set(BaseScheme):
    scores: Optional[List[int]] = None


class Discipline(BaseScheme):
    play_id: str = Field(..., alias='playId')
    sets: Optional[List[Set]] = []


class Match(BaseScheme):
    """Матч"""
    time_start: Optional[datetime] = Field(..., alias='timeStart')
    time_end: Optional[datetime] = Field(..., alias='timeEnd')
    team1: Optional[Team]
    team2: Optional[Team]
    result: List[int]
    is_elimination: Optional[bool] = Field(..., alias='eliminationMatch')
    disciplines: List[Discipline]
    deactivated: bool


class Round(BaseScheme):
    matches: List[Match]


class Qualifying(BaseScheme):
    """Квалификация"""
    participants: List[Player]
    standings: List[Standings]
    rounds: List[Round]


class Level(BaseScheme):
    matches: List[Match]


class Elimination(BaseScheme):
    """Плей офф"""
    size: int
    standings: List[Standings]
    left_levels: List[Level] = Field(..., alias='leftLevels')
    levels: List[Level]
    third: Level


class DYPScheme(BaseScheme):
    name: str
    created_at: datetime = Field(..., alias='createdAt')
    qualifying: List[Qualifying]
    eliminations: List[Elimination]


class BaseDYP(BaseCompetition):
    json_data: DYPScheme


class CreateDYP(BaseDYP):
    json_data: Json[Any]


class ResponseDYPCompetition(BaseDYP):
    id: int
