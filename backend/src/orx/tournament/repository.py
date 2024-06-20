from src.core.repository import SqlAlchemyRepository
from src.models import TournametModel, TournametTeamModel

from .schemas import (
    CreateTournament,
    UpdateTournament,
    PartialTournament,
    CreateTournamentTeam,
    UpdateTournamentTeam,
    PartialTournamentTeam
)


class TournamentsRepository(
    SqlAlchemyRepository[TournametModel, CreateTournament, UpdateTournament, PartialTournament]
):
    model = TournametModel


class TournamentTeamsRepository(
    SqlAlchemyRepository[TournametTeamModel, CreateTournamentTeam, UpdateTournamentTeam, PartialTournamentTeam]
):
    model = TournametTeamModel
