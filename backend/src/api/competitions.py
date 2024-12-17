from typing import List
import json
from fastapi import APIRouter

from src.orx.competition.depends import CompetitionDep
from src.orx.competition.schemas import ResponseCompetition, ResponceCompetitionInfo


router = APIRouter(
    prefix="/competition",
    tags=["Competitions"],
)


@router.get("")
async def list_competitions(service: CompetitionDep) -> List[ResponseCompetition]:
    """Список игроков"""
    return await service.list()


@router.get('/{competition_id}')
async def get_competition_info(service: CompetitionDep, competition_id: int) -> ResponceCompetitionInfo:
    return await service.get_competition_info(competition_id)

