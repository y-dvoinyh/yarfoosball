from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.model import BaseModel


class PlayerModel(BaseModel):
    __tablename__ = "players"

    first_name: Mapped[str] = mapped_column(String(20), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), unique=False, nullable=False)
