"""API Запуска расчета рейтинга"""
from typing import List, Optional
from fastapi import APIRouter

from src.orx.rating.depends import RatingDep
from src.orx.rating.calculate.depends import RatingCalculateDep
from src.orx.rating.schemas import ResponseRating, ResponseRatingList


router = APIRouter(
    prefix="/rating",
    tags=["Rating"],
)


@router.get("")
async def list_ratings(
        service: RatingDep,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        search_string: Optional[str] = None
) -> ResponseRatingList:
    """Список рейтингов"""
    if limit == 0:
        limit = None
    return await service.rating_list_with_count(limit, offset, search_string)


@router.get("/calculate")
async def calculate_rating(service: RatingDep, competition_id: Optional[int] = None) -> bool:
    """Запуск расчета рейтинга игроков"""
    return await service.calculate_rating(competition_id)


@router.get("/new_calculate")
async def new_calculate_rating(service: RatingCalculateDep) -> Optional[bool]:
    """Запуск расчета рейтинга игроков (Новая версия)"""
    return await service.calculate()
