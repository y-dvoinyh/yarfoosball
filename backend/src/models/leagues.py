from typing import TYPE_CHECKING, List

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.model import BaseModel

if TYPE_CHECKING:
    from .tournaments import TournametModel


class LeagueModel(BaseModel):
    """Лига"""
    __tablename__ = "leagues"

    name: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Турниры
    tournaments: Mapped[List["TournametModel"]] = relationship(back_populates="league")

    def __str__(self):
        return f'League: {self.id} - "{self.name}"'
