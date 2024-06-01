from typing import List
from fastapi import APIRouter

from src.modules.players.schemas import CreatePlayer, ResponsePlayer
from src.modules.players.depends import PlayersDep


router = APIRouter(
    prefix="/players",
    tags=["Players"],
)


@router.post("")
async def create_player(player_data: CreatePlayer, pleyer_service: PlayersDep) -> ResponsePlayer:
    """Создать игрока"""
    return await pleyer_service.create(player_data)


@router.get("")
async def list_players(pleyer_service: PlayersDep) -> List[ResponsePlayer]:
    """Список игроков"""
    return await pleyer_service.list()
