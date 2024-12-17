from src.core.uow import UnitOfWork
from .repository import CompetitionsRepository


class UnitOfWorkCompetitions(UnitOfWork):
    repository: CompetitionsRepository

    def __init__(self):
        super(UnitOfWorkCompetitions, self).__init__()
        self.repository = CompetitionsRepository(self.session)
