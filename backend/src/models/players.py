from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.model import BaseModel


class PlayerModel(BaseModel):
    """Игрок"""
    __tablename__ = "players"

    first_name: Mapped[str] = mapped_column(String(20), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), unique=False, nullable=False)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"Player: {self.id} {self.last_name} {self.first_name}"
