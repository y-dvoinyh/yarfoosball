"""API загрузки из Командной лиги"""
from typing import List
import json
from fastapi import APIRouter, File

from src.models.enums import TournamentType

from src.orx.team_tournament.depends import TeamTournamentDep
from src.orx.team_tournament.schemas import ResponseTeamTournament


router = APIRouter(
    prefix="/team_tournament",
    tags=["Team Tournament"],
)


@router.post("/upload")
async def upload_file_json(
        service: TeamTournamentDep,
        league_id: int,
        file_bytes: bytes = File()
) -> ResponseTeamTournament:
    return await service.load_from_json(league_id, file_bytes)


@router.get("")
async def list_team_tournaments(service: TeamTournamentDep) -> List[ResponseTeamTournament]:
    """Список игроков"""
    filters = {'type': TournamentType.TEAM}
    return await service.list(**filters)
