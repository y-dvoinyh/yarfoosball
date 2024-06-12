from typing import List
import json
from fastapi import APIRouter

from src.modules.competition.depends import CompetitionDep
from src.modules.competition.schemas import ResponseCompetition


router = APIRouter(
    prefix="/competition",
    tags=["Competitions"],
)


@router.get("")
async def list_competitions(service: CompetitionDep) -> List[ResponseCompetition]:
    """Список игроков"""
    return await service.list()

