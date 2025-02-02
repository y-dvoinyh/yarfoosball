from typing import Optional, List
from pydantic import BaseModel

from src.models import HistoryRatingLevel, RatingType, Rank
from src.core.constants import DEFAULT_RATING


class BaseRating(BaseModel):
    type: RatingType
    player_id: int
    rating: int
    league_id: Optional[int] = None
    tournament_id: Optional[int] = None

    tournaments: Optional[int] = 0
    matches: Optional[int] = 0
    wins: Optional[int] = 0
    losses: Optional[int] = 0
    goals: Optional[int] = 0
    last_diff: Optional[int] = 0
    rank: Optional[Rank] = Rank.beginner
    cumulative: Optional[int] = 0


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
    level: HistoryRatingLevel
    player_id: int

    prev_history_id: Optional[int] = None
    league_id: Optional[int] = None
    tournament_id: Optional[int] = None
    competition_id: Optional[int] = None
    match_id: Optional[int] = None

    rating: Optional[int] = DEFAULT_RATING
    diff: Optional[int] = 0

    matches: Optional[int] = 0
    matches_diff: Optional[int] = 0
    wins: Optional[int] = 0
    wins_diff: Optional[int] = 0
    losses: Optional[int] = 0
    losses_diff: Optional[int] = 0

    goals: Optional[int] = 0
    goals_diff: Optional[int] = 0

    tournaments: Optional[int] = 0

    rank: Optional[Rank] = Rank.beginner

    cumulative: Optional[int] = 0
    cumulative_diff: Optional[int] = 0


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
    competition_id: Optional[int] = None
    match_id: Optional[int] = None

    rating: Optional[int] = None
    diff: Optional[int] = None


class ResponseRatingPlayer(BaseModel):
    player_id: int
    full_name: str
    number: int
    rating: int
    matches: int
    wins: int
    losses: int
    last_diff: Optional[int] = 0
    goals: Optional[int] = 0
    tournaments: Optional[int] = 0
    rank: Optional[str] = 'novice'
    color: Optional[str] = 'grey'
    cumulative: Optional[int] = 0


class ResponseRatingList(BaseModel):
    """Список игроков с рейтингом"""
    count: int
    players: List[ResponseRatingPlayer]