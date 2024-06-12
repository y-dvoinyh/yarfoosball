from typing import Annotated
from fastapi import Depends

from src.core.depends import UOWDep

from .service import TournamentService


def get_tournament_service(uow: UOWDep):
    return TournamentService(uow)


TournamentsDep = Annotated[TournamentService, Depends(get_tournament_service)]
