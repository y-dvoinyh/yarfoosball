"""API загрузки из kickertool"""
from typing import List
from fastapi import APIRouter, File

from src.models.enums import CompetitionType
from src.orx.kickertool.schemas import ResponseDYPCompetition
from src.orx.kickertool.depends import KickerToolDep


router = APIRouter(
    prefix="/kickertool",
    tags=["Kickertool"],
)


@router.post("/dyp/upload")
async def upload_file_json(
        service: KickerToolDep,
        tournament_id: int,
        file_bytes: bytes = File()
) -> ResponseDYPCompetition:
    return await service.load_from_json(tournament_id, file_bytes)


@router.get("")
async def list_competitions(service: KickerToolDep) -> List[ResponseDYPCompetition]:
    """Список игроков"""
    filters = {'type': CompetitionType.DYP}
    return await service.list(**filters)

