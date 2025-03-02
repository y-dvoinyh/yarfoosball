"""API загрузки из kickertool"""
from typing import List
from fastapi import APIRouter, File

from src.models import CompetitionType
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


@router.get("/dyp/load_by_link")
async def load_by_live_link(service: KickerToolDep, link: str) -> bool:
    return await service.load_by_live_link(link)


@router.get("")
async def list_competitions(service: KickerToolDep) -> List[ResponseDYPCompetition]:
    """Список игроков"""
    filters = {'type': CompetitionType.DYP}
    return await service.list(**filters)

@router.post('/dyp/update_standins')
async def update_standings(service: KickerToolDep) -> bool:
    return await service.update_competitition_standins()
