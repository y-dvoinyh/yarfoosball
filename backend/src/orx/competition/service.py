from src.core.service import BaseService


class CompetitionService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = self.uow.competitions
