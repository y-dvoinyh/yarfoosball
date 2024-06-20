from typing import Annotated
from fastapi import Depends

from src.core.depends import UOWDep

from .service import CompetitionService


def get_competition_service(uow: UOWDep):
    return CompetitionService(uow)


CompetitionDep = Annotated[CompetitionService, Depends(get_competition_service)]
