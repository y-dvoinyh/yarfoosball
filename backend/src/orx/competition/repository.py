from sqlalchemy import select

from src.core.repository import SqlAlchemyRepository
from src.models import CompetitionModel

from .schemas import CreateCompetition, UpdateCompetition, PartialCompetition


class CompetitionsRepository(
    SqlAlchemyRepository[CompetitionModel, CreateCompetition, UpdateCompetition, PartialCompetition]
):
    model = CompetitionModel

    async def get_competition_info(self, competition_id: int):
        stmt = select(
            self.model.id,
            self.model.name,
            self.model.date
        ).where(
                self.model.id == competition_id
        )
        row = await self._session.execute(stmt)
        return row.first()
