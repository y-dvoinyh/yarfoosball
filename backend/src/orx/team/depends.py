from typing import Annotated
from fastapi import Depends

from src.core.depends import UOWDep

from .service import TeamsService


def get_team_service(uow: UOWDep):
    return TeamsService(uow)


TeamsDep = Annotated[TeamsService, Depends(get_team_service)]
