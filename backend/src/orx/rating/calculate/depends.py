from typing import Annotated
from fastapi import Depends

from src.core.depends import UOWDep

from .rating import Rating
from .service import RatingService


def __get_rating_calculate_service(uow: UOWDep):
    return Rating(RatingService(uow))


RatingCalculateDep = Annotated[Rating, Depends(__get_rating_calculate_service)]

