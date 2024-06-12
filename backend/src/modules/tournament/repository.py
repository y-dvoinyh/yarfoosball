from src.core.repository import SqlAlchemyRepository
from src.models.tournaments import TournametModel

from .schemas import CreateTournament, UpdateTournament, PartialTournament


class TournamentsRepository(
    SqlAlchemyRepository[TournametModel, CreateTournament, UpdateTournament, PartialTournament]
):
    model = TournametModel
