from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import Enum, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.model import BaseModel

from .enums import CompetitionType

if TYPE_CHECKING:
    from tournaments import TournametModel


class CompetitionModel(BaseModel):
    """Соревнование"""
    __tablename__ = "competitions"
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    type: Mapped[CompetitionType] = mapped_column(Enum(CompetitionType, name='competition_type_enum'), nullable=False)

    # Турнир
    tournament_id: Mapped[int] = mapped_column(
        ForeignKey('tournaments.id', ondelete='CASCADE'),
        unique=False,
        nullable=False,
    )
    tournament: Mapped['TournametModel'] = relationship(back_populates="competitions")

    def __str__(self):
        return f'Tournament: {self.id} - "{self.name}"'
