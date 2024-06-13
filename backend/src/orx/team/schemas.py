from typing import Optional
from pydantic import BaseModel


class BaseTeam(BaseModel):
    external_id: Optional[str]
    competition_order: Optional[int]
    competition_id: int
    first_player_id: int
    second_player_id: Optional[int]


class ResponseTeam(BaseTeam):
    id: int


class CreateTeam(BaseTeam):
    ...


class UpdateTeam(BaseTeam):
    ...


class PartialTeam(BaseTeam):
    external_id: Optional[str] = None
    competition_order: Optional[int] = None
    competition_id: Optional[int] = None
    first_player_id: Optional[int] = None
    second_player_id: Optional[int] = None
