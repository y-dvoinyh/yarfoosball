from typing import List, Optional
from fastapi import APIRouter

from src.orx.player.schemas import CreatePlayer, ResponsePlayer, UpdatePlayer, ResponsePlayerCompetitionList, \
    ResponcePlayerInfo, ResponceMatchRow, PartnerResponce
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


@router.get('/competitions')
async def get_player_competitions(
    service: PlayersDep,
    player_id: int,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    search_string: Optional[str] = None
) -> ResponsePlayerCompetitionList:
    if limit == 0:
        limit = None
    return await service.competitions_list(player_id, limit, offset, search_string)


@router.get('/player/{player_id}/competition/{competition_id}')
async def get_player_competition(
    service: PlayersDep,
    player_id: int,
    competition_id: int
) -> List[ResponceMatchRow]:
    return await service.player_competition(player_id, competition_id)


@router.get('/{player_id}')
async def get_player_info(service: PlayersDep, player_id: int) -> ResponcePlayerInfo:
    return await service.get_player_info(player_id)


@router.get('/partners/{player_id}')
async def get_partners(service: PlayersDep, player_id: int) -> List[PartnerResponce]:
    return await service.get_partners(player_id)


@router.get('/opponents/{player_id}')
async def get_popponents(service: PlayersDep, player_id: int) -> List[PartnerResponce]:
    return await service.get_opponents(player_id)