from src.core.repository import SqlAlchemyRepository
from src.models import CompetitionModel

from .schemas import CreateCompetition, UpdateCompetition, PartialCompetition


class CompetitionsRepository(
    SqlAlchemyRepository[CompetitionModel, CreateCompetition, UpdateCompetition, PartialCompetition]
):
    model = CompetitionModel
