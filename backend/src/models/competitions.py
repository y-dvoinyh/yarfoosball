from datetime import date
from typing import TYPE_CHECKING, List
from sqlalchemy import Enum, Text, Date, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.model import BaseModel

from .enums import CompetitionType

if TYPE_CHECKING:
    from .tournaments import TournametModel
    from .teams import TeamModel


class CompetitionModel(BaseModel):
    """Соревнование"""
    __tablename__ = "competitions"
    external_id: Mapped[str] = mapped_column(String(30), unique=False, nullable=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    type: Mapped[CompetitionType] = mapped_column(Enum(CompetitionType, name='competition_type_enum'), nullable=False)

    json_data = mapped_column(JSON)

    # Турнир
    tournament_id: Mapped[int] = mapped_column(
        ForeignKey('tournaments.id', ondelete='CASCADE'),
        unique=False,
        nullable=False,
    )
    tournament: Mapped['TournametModel'] = relationship(
        foreign_keys="CompetitionModel.tournament_id",
        back_populates="competitions"
    )
    # Команды
    teams: Mapped[List['TeamModel']] = relationship(back_populates="competition")

    def __str__(self):
        return f'Tournament: {self.id} - "{self.name}"'
