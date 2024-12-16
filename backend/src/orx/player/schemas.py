from datetime import date
from typing import Optional, List
from pydantic import BaseModel


class BasePlayer(BaseModel):
    first_name: str
    last_name: str


class ResponsePlayer(BasePlayer):
    id: int


class CreatePlayer(BasePlayer):
    ...


class UpdatePlayer(BasePlayer):
    ...


class PartialPlayer(BasePlayer):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class ResponsePlayerCompetition(BaseModel):
    id: int
    name: str
    date: date
    rating: Optional[int]
    diff: Optional[int]
    matches_diff: Optional[int]
    wins_diff: Optional[int]
    losses_diff: Optional[int]


class ResponsePlayerCompetitionList(BaseModel):
    """Список игроков с рейтингом"""
    count: int
    competitions: List[ResponsePlayerCompetition]


class ResponcePlayerInfo(BaseModel):
    rating: int
    matches: int
    wins: int
    losses: int
    first_name: str
    last_name: str
