from typing import Optional, Any
from datetime import date
from pydantic import BaseModel, Json

from src.models import CompetitionType


class BaseCompetition(BaseModel):
    tournament_id: int
    name: str
    description: str
    date: date
    type: CompetitionType
    external_id: Optional[str]


class ResponseCompetition(BaseCompetition):
    id: int


class CreateCompetition(BaseCompetition):
    ...


class UpdateCompetition(BaseCompetition):
    ...


class PartialCompetition(BaseCompetition):
    name: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None
    type: Optional[CompetitionType] = None
    json_data: Optional[Json[Any]] = None
    tournament_id: Optional[int] = None
    external_id: Optional[str] = None
