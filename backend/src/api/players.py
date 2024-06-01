from typing import List
from fastapi import APIRouter

from src.modules.player.schemas import CreatePlayer, ResponsePlayer
from src.modules.player.depends import PlayersDep


router = APIRouter(
    prefix="/player",
    tags=["Players"],
)


@router.post("")
async def create_player(player_data: CreatePlayer, service: PlayersDep) -> ResponsePlayer:
    """Создать игрока"""
    return await service.create(player_data)


@router.get("")
async def list_players(service: PlayersDep) -> List[ResponsePlayer]:
    """Список игроков"""
    return await service.list()
