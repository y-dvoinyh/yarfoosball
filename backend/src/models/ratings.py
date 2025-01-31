from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.constants import DEFAULT_RATING
from src.core.model import BaseModel

from .enums import RatingType, HistoryRatingLevel, Rank

if TYPE_CHECKING:
    from .players import PlayerModel
    from .leagues import LeagueModel
    from .tournaments import TournametModel
    from .competitions import CompetitionModel
    from .matches import MatchModel


class RatingModel(BaseModel):
    """Рейтинг"""
    __tablename__ = "ratings"

    type: Mapped[RatingType] = mapped_column(Enum(RatingType, name='rating_type_enum'), nullable=False)

    player_id: Mapped[int] = mapped_column(ForeignKey('players.id'), nullable=False)
    player: Mapped["PlayerModel"] = relationship(foreign_keys="RatingModel.player_id", lazy='joined')

    league_id: Mapped[int] = mapped_column(ForeignKey('leagues.id'), nullable=True)
    league: Mapped["LeagueModel"] = relationship(foreign_keys="RatingModel.league_id")

    tournament_id: Mapped[int] = mapped_column(ForeignKey('tournaments.id'), nullable=True)
    tournament: Mapped["TournametModel"] = relationship(foreign_keys="RatingModel.tournament_id")

    rank: Mapped[Rank] = mapped_column(Enum(Rank, name='rank_enum'), nullable=True)

    rating: Mapped[int] = mapped_column(Integer, default=DEFAULT_RATING, nullable=False)

    tournaments: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    matches: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    wins: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    losses: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    goals: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)

    last_diff: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)


class RatingHistoryModel(BaseModel):
    """История изменения рейтинга"""
    __tablename__ = "rating_history"

    type: Mapped[RatingType] = mapped_column(Enum(RatingType, name='rating_type_enum'), nullable=False)
    level: Mapped[HistoryRatingLevel] = mapped_column(
        Enum(HistoryRatingLevel, name='rating_history_level_enum'), nullable=False)

    prev_history_id: Mapped[int] = mapped_column(ForeignKey('rating_history.id'), nullable=True)
    prev_history: Mapped["RatingHistoryModel"] = relationship(
        foreign_keys="RatingHistoryModel.prev_history_id")

    league_id: Mapped[int] = mapped_column(ForeignKey('leagues.id'), nullable=True)
    league: Mapped["LeagueModel"] = relationship(foreign_keys="RatingHistoryModel.league_id")

    tournament_id: Mapped[int] = mapped_column(ForeignKey('tournaments.id'), nullable=True)
    tournament: Mapped["TournametModel"] = relationship(foreign_keys="RatingHistoryModel.tournament_id")

    player_id: Mapped[int] = mapped_column(ForeignKey('players.id'), nullable=False)
    player: Mapped["PlayerModel"] = relationship(foreign_keys="RatingHistoryModel.player_id")

    competition_id: Mapped[int] = mapped_column(ForeignKey('competitions.id'), nullable=True)
    competition: Mapped["CompetitionModel"] = relationship(
        foreign_keys="RatingHistoryModel.competition_id",
        back_populates="ratings"
    )

    match_id: Mapped[int] = mapped_column(ForeignKey('matches.id'), nullable=True)
    match: Mapped["MatchModel"] = relationship(foreign_keys="RatingHistoryModel.match_id")

    rating: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    diff: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)

    tournaments: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    matches: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    matches_diff: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    wins: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    wins_diff: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    losses: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    losses_diff: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    goals: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    goals_diff: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)

    place: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    rank: Mapped[Rank] = mapped_column(Enum(Rank, name='rank_enum'), nullable=True)