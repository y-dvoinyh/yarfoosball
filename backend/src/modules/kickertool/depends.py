from typing import Annotated
from fastapi import Depends

from src.core.depends import UOWDep

from .service import KickerToolDYPService


def get_kickertool_service(uow: UOWDep):
    return KickerToolDYPService(uow)


KickerToolDep = Annotated[KickerToolDYPService, Depends(get_kickertool_service)]
