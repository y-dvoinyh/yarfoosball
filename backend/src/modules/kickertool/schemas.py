from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from src.modules.competition.schemas import BaseCompetition, CreateCompetition, ResponseCompetition


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
    scores: List[int]


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


class Round(BaseScheme):
    matches: List[Match]


class Qualifying(BaseScheme):
    """Квалификация"""
    participants: List[Player]
    standings: List[Standings]
    rounds: List[Round]


class Level(BaseScheme):
    hash: str
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

    players_dict: Optional[dict] = {}
    __all_teams: Optional[dict] = None

    def add_player(self, id: str, player):
        self.players_dict[id] = player

    def get_player(self, id: str):
        return self.players_dict.get(id)

    @property
    def all_teams(self) -> List[Team]:
        return [t for t in self.dict_teams.values()]

    @property
    def dict_teams(self) -> dict:
        if self.__all_teams is None:
            self.__all_teams = {}
        return self.__all_teams

    def get_team(self, id: str) -> Optional[Team]:
        return self.dict_teams.get(id)


class BaseDYP(BaseCompetition):
    json_data: DYPScheme


class CreateDYP(BaseDYP):
    ...


class ResponseDYPCompetition(BaseDYP):
    id: int
