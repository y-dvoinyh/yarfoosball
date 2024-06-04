from typing import TYPE_CHECKING, List

from sqlalchemy import String, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.model import BaseModel

from .enums import TournamentType

if TYPE_CHECKING:
    from .leagues import LeagueModel
    from .competitions import CompetitionModel


class TournametModel(BaseModel):
    """Турнир"""
    __tablename__ = "tournaments"

    name: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    type: Mapped[TournamentType] = mapped_column(Enum(TournamentType, name='tournament_type_enum'), nullable=False)

    league_id: Mapped[int] = mapped_column(
        ForeignKey("leagues.id", ondelete="CASCADE"),
        unique=False,
        nullable=False,
    )
    league: Mapped["LeagueModel"] = relationship(
        foreign_keys="TournametModel.league_id",
        back_populates="tournaments"
    )
    # Соревнования
    competitions: Mapped[List['CompetitionModel']] = relationship(back_populates="tournament")

    def __str__(self):
        return f'Tournament: {self.id} - "{self.name}"'
