from src.core.service import BaseService


class CompetitionService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = self.uow.competitions

    async def get_competition_info(self, competition_id: int):
        return await self.repository.get_competition_info(competition_id)