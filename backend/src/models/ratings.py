from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.core.model import BaseModel

from .enums import RatingType


class RatingModel(BaseModel):
    """Рейтинги"""
    __tablename__ = "ratings"

    type: Mapped[RatingType] = mapped_column(
        Enum(RatingType, name='rating_type_enum'),
        nullable=False,
        default=RatingType.PLAYER
    )


