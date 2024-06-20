from typing import List
from fastapi import APIRouter

from src.orx.player.schemas import CreatePlayer, ResponsePlayer, UpdatePlayer
from src.orx.player.depends import PlayersDep


router = APIRouter(
    prefix="/players",
    tags=["Players"],
)


@router.post("")
async def create_player(player_data: CreatePlayer, service: PlayersDep) -> ResponsePlayer:
    """Создать игрока"""
    return await service.create(player_data)


@router.post("/update")
async def update_player(player_id: int, player_data: UpdatePlayer, service: PlayersDep) -> ResponsePlayer:
    """Создать игрока"""
    return await service.update(player_data, **{'id': player_id})


@router.get("")
async def list_players(service: PlayersDep) -> List[ResponsePlayer]:
    """Список игроков"""
    return await service.list()
