from typing import Annotated
from fastapi import Depends

from src.core.depends import UOWDep

from .service import RatingService, RatingHistoryService


def get_rating_service(uow: UOWDep):
    return RatingService(uow)


def get_rating_history_service(uow: UOWDep):
    return RatingHistoryService(uow)


RatingDep = Annotated[RatingService, Depends(get_rating_service)]
RatingHistoryDep = Annotated[RatingHistoryService, Depends(get_rating_history_service)]
