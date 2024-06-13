from typing import Annotated
from fastapi import Depends

from src.core.depends import UOWDep

from .service import TournamentService, TournamentTeamService


def get_tournament_service(uow: UOWDep):
    return TournamentService(uow)


def get_tournament_team_service(uow: UOWDep):
    return TournamentTeamService(uow)


TournamentsDep = Annotated[TournamentService, Depends(get_tournament_service)]
TournamentTeamsDep = Annotated[TournamentTeamService, Depends(get_tournament_team_service)]
