from typing import List
import json
from fastapi import APIRouter

from src.orx.competition.depends import CompetitionDep
from src.orx.competition.schemas import ResponseCompetition


router = APIRouter(
    prefix="/competition",
    tags=["Competitions"],
)


@router.get("")
async def list_competitions(service: CompetitionDep) -> List[ResponseCompetition]:
    """Список игроков"""
    return await service.list()

