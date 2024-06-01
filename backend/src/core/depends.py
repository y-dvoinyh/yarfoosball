from typing import Annotated
from fastapi import Depends
from .uow import UnitOfWork


async def get_unit_of_work():
    uow = UnitOfWork()
    try:
        yield uow
    finally:
        await uow.session.close()

    await uow.rollback()
    await uow.session.close()


UOWDep = Annotated[UnitOfWork, Depends(get_unit_of_work)]
