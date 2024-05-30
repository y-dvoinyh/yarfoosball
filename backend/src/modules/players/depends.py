from typing import Annotated
from fastapi import Depends

from src.core.depends import UOWDep

from .service import PlayersService


def get_player_service(uow: UOWDep):
    return PlayersService(uow)


PlayersDep = Annotated[PlayersService, Depends(get_player_service)]
