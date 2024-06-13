from typing import Annotated
from fastapi import Depends

from src.core.depends import UOWDep

from .service import MatchService, SetService


def get_match_service(uow: UOWDep):
    return MatchService(uow)


def get_set_service(uow: UOWDep):
    return SetService(uow)


TeamsDep = Annotated[MatchService, Depends(get_match_service)]
SetsDep = Annotated[SetService, Depends(get_set_service)]
