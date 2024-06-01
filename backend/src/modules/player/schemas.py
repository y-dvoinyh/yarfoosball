from typing import Optional
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
