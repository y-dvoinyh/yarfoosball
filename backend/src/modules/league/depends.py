from typing import Annotated
from fastapi import Depends

from src.core.depends import UOWDep

from .service import LeagueService


def get_league_service(uow: UOWDep):
    return LeagueService(uow)


LeagueDep = Annotated[LeagueService, Depends(get_league_service)]
