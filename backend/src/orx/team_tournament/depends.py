from typing import Annotated
from fastapi import Depends

from src.core.depends import UOWDep

from .service import TeamTournamentService


def get_team_tournament_service(uow: UOWDep):
    return TeamTournamentService(uow)


TeamTournamentDep = Annotated[TeamTournamentService, Depends(get_team_tournament_service)]
