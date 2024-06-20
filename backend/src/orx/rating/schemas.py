from typing import Optional, List
from pydantic import BaseModel

from src.models import HistoryRatingLevel, RatingType
from src.core.constants import DEFAULT_RATING


class BaseRating(BaseModel):
    type: RatingType
    player_id: int
    rating: int
    league_id: Optional[int] = None
    tournament_id: Optional[int] = None


class ResponseRating(BaseRating):
    id: int


class CreateRating(BaseRating):
    rating:  Optional[int] = None


class UpdateRating(BaseRating):
    ...


class PartialRating(BaseRating):
    type: Optional[RatingType] = None
    player_id: Optional[int] = None
    rating: Optional[int] = None


class BaseRatingHistory(BaseModel):
    type: RatingType
    prev_history_id: Optional[int] = None
    level: HistoryRatingLevel
    player_id: int
    match_id: Optional[int]

    rating: int
    diff: int


class ResponseRatingHistory(BaseRatingHistory):
    id: int


class CreateRatingHistory(BaseRatingHistory):
    ...


class UpdateRatingHistory(BaseRatingHistory):
    ...


class PartialRatingHistory(BaseRatingHistory):
    type: Optional[RatingType] = None
    prev_history_id: Optional[int] = None
    level: Optional[HistoryRatingLevel] = None
    player_id: Optional[int] = None
    match_id: Optional[int] = None

    rating: Optional[int] = None
    diff: Optional[int] = None


class ResponseRatingPlayer(BaseModel):
    number: int
    rating: int
    full_name: str


class ResponseRatingList(BaseModel):
    """Список игроков с рейтингом"""
    count: int
    players: List[ResponseRatingPlayer]