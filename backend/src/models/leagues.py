from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.model import BaseModel


class LeagueModel(BaseModel):
    __tablename__ = "leagues"

    name: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    def __str__(self):
        return f'League: {self.id} - "{self.name}"'
