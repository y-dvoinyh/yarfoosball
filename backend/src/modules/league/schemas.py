from typing import Optional
from pydantic import BaseModel


class BaseLeague(BaseModel):
    name: str
    description: str


class ResponseLeague(BaseLeague):
    id: int


class CreateLeague(BaseLeague):
    ...


class UpdateLeague(BaseLeague):
    ...


class PartialLeague(BaseLeague):
    name: Optional[str] = None
    description: Optional[str] = None
