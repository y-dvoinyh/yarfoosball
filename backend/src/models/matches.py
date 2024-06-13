from typing import TYPE_CHECKING, List
from datetime import datetime
from sqlalchemy import ForeignKey, Integer, Boolean, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.model import BaseModel

if TYPE_CHECKING:
    from .competitions import CompetitionModel
    from .teams import TeamModel


class MatchModel(BaseModel):
    """Матч"""
    __tablename__ = "matches"
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    # Соревнование
    competition_id: Mapped[int] = mapped_column(ForeignKey('competitions.id'), nullable=False)
    competition: Mapped["CompetitionModel"] = relationship(foreign_keys="MatchModel.competition_id", lazy='joined')

    first_team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'), nullable=False)
    first_team: Mapped["TeamModel"] = relationship(foreign_keys="MatchModel.first_team_id", lazy='joined')

    second_team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'), nullable=False)
    second_team: Mapped["TeamModel"] = relationship(foreign_keys="MatchModel.first_team_id", lazy='joined')

    is_qualification: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_forfeit: Mapped[bool] = mapped_column(Boolean, nullable=True)

    time_start: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    sets: Mapped[List['MatchSetModel']] = relationship(back_populates="match")

    @property
    def teams(self) -> list['TeamModel']:
        return [self.first_team, self.second_team]

    @property
    def is_singles(self) -> bool:
        return self.first_team.is_single_player


class MatchSetModel(BaseModel):
    """Сет"""
    __tablename__ = "match_sets"
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    match_id: Mapped[int] = mapped_column(ForeignKey('matches.id'), nullable=False)
    match: Mapped["MatchModel"] = relationship(foreign_keys="MatchSetModel.match_id", lazy='joined')
    first_team_score:  Mapped[int] = mapped_column(Integer, nullable=False)
    second_team_score:  Mapped[int] = mapped_column(Integer, nullable=False)

    @property
    def is_first_team_win(self) -> bool:
        return self.first_team_score > self.second_team_score
