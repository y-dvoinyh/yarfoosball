from typing import List
from src.core.service import BaseService
from src.models import CompetitionModel
from ..schemas import CreateRatingHistory
from ..repository import RatingRepository


class RatingService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository: RatingRepository = self.uow.ratings

    async def competitions(self) -> List[CompetitionModel]:
        return await self.uow.competitions.all(order="date")

    async def get_rating_history(self, **filters):
        return await self.uow.rating_history.get_single(**filters)

    async def create_rating_history(self, data: CreateRatingHistory):
        return await self.uow.rating_history.create(data)
