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


class ResponceMatchRow(BaseModel):
    id: int
    is_qualification: bool
    rating: int
    diff: Optional[int]
    score: Optional[str]
    color: Optional[str]
    left_team_first_id: Optional[int]
    left_team_first: Optional[str]
    left_team_second_id: Optional[int]
    left_team_second: Optional[str]
    right_team_first_id: Optional[int]
    right_team_first: Optional[str]
    right_second_id: Optional[int]
    right_second: Optional[str]


class PartnerResponce(BaseModel):
    id: int
    is_win: bool
    is_losse: bool
    count: int
    name: str
