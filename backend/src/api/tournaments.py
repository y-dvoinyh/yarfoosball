from typing import List
from fastapi import APIRouter

from src.modules.tournament.depends import TournamentsDep
from src.modules.tournament.schemas import ResponseTournament, CreateTournament


router = APIRouter(
    prefix="/tournament",
    tags=["Tournamens"],
)


@router.post("")
async def create(data: CreateTournament, service: TournamentsDep) -> ResponseTournament:
    """Создать лигу"""
    return await service.create(data)


@router.get("")
async def list_tournaments(service: TournamentsDep) -> List[ResponseTournament]:
    """Список игроков"""
    return await service.list()
