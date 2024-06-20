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
    competition: Mapped["CompetitionModel"] = relationship(
        foreign_keys="MatchModel.competition_id", lazy='joined', back_populates="matches"
    )

    first_team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'), nullable=False)
    first_team: Mapped["TeamModel"] = relationship(foreign_keys="MatchModel.first_team_id", lazy='joined')

    second_team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'), nullable=False)
    second_team: Mapped["TeamModel"] = relationship(foreign_keys="MatchModel.second_team_id", lazy='joined')

    is_qualification: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_forfeit: Mapped[bool] = mapped_column(Boolean, nullable=True)

    time_start: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    sets: Mapped[List['MatchSetModel']] = relationship(back_populates="match", lazy='selectin')

    @property
    def teams(self) -> list['TeamModel']:
        """Команды матча"""
        return [self.first_team, self.second_team]

    @property
    def is_draw(self):
        """Ничья"""
        return all([set_.is_draw for set_ in self.sets])

    @property
    def winner(self) -> 'TeamModel':
        """Победитель команда"""
        return self.first_team if self.is_first_team_win else self.second_team

    @property
    def looser(self) -> 'TeamModel':
        """Проигравшая команда"""
        return self.second_team if self.is_first_team_win else self.first_team

    @property
    def winner_score(self):
        return self.first_team_score if self.is_first_team_win else self.second_team_score

    @property
    def looser_score(self):
        return self.second_team_score if self.is_first_team_win else self.first_team_score

    @property
    def is_first_team_win(self) -> bool:
        return sum([1 if set_.is_first_team_win else -1 for set_ in self.sets]) > 0

    @property
    def is_single_set(self) -> bool:
        return len(self.sets) <= 1

    @property
    def first_team_score(self):
        if self.is_single_set:
            return self.sets[0].first_team_score
        return sum([1 if set_.first_team_score > set_.second_team_score else 0 for set_ in self.sets])

    @property
    def second_team_score(self):
        if self.is_single_set:
            return self.sets[0].second_team_score
        return sum([1 if set_.second_team_score > set_.first_team_score else 0 for set_ in self.sets])

    @property
    def is_singles(self) -> bool:
        return self.first_team.is_single_player

    def __str__(self):
        return f'Match: {str(self.order)} - {self.id}: {str(self.time_start)}"'


class MatchSetModel(BaseModel):
    """Сет"""
    __tablename__ = "match_sets"
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    match_id: Mapped[int] = mapped_column(ForeignKey('matches.id'), nullable=False)
    match: Mapped["MatchModel"] = relationship(foreign_keys="MatchSetModel.match_id", lazy='joined')
    first_team_score:  Mapped[int] = mapped_column(Integer, nullable=False)
    second_team_score:  Mapped[int] = mapped_column(Integer, nullable=False)

    @property
    def is_first_team_win(self) -> bool | None:
        return self.first_team_score > self.second_team_score

    @property
    def is_draw(self):
        return self.first_team_score == self.second_team_score

    def __str__(self):
        return f'Set: {str(self.order)} - {self.id}: [{self.first_team_score} - "{self.second_team_score}]"'
