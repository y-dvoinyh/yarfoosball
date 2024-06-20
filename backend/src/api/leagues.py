from typing import List
from fastapi import APIRouter

from src.orx.league.schemas import CreateLeague, ResponseLeague
from src.orx.league.depends import LeagueDep


router = APIRouter(
    prefix="/league",
    tags=["Leagues"],
)


@router.post("")
async def create_league(league_data: CreateLeague, service: LeagueDep) -> ResponseLeague:
    """Создать лигу"""
    return await service.create(league_data)


@router.get("")
async def list_leagues(service: LeagueDep) -> List[ResponseLeague]:
    """Список игроков"""
    return await service.list()
