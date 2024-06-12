from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class BaseMatch(BaseModel):
    external_id: Optional[str]
    order: Optional[int]
    competition_id: int
    first_team_id: int
    second_team_id: int
    is_qualification: Optional[bool]
    time_start: Optional[datetime]


class ResponseMatch(BaseMatch):
    id: int


class CreateMatch(BaseMatch):
    ...


class UpdateMatch(BaseMatch):
    ...


class PartialMatch(BaseMatch):
    external_id: Optional[str] = None
    order: Optional[int] = None
    competition_id: Optional[int] = None
    first_team_id: Optional[int] = None
    second_team_id: Optional[int] = None
    is_qualification: Optional[bool] = None
    time_start: Optional[datetime] = None


class BaseSet(BaseModel):
    external_id: Optional[str]
    order: Optional[int]
    match_id: int
    first_team_score: int
    second_team_score: int


class ResponseSet(BaseSet):
    id: int


class CreateSet(BaseSet):
    ...


class UpdateSet(BaseSet):
    ...


class PartialSet(BaseSet):
    external_id: Optional[str] = None
    order: Optional[int] = None
    match_id: Optional[int] = None
    first_team_score: Optional[int] = None
    second_team_score: Optional[int] = None
