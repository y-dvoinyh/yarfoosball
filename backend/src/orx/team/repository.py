from src.core.repository import SqlAlchemyRepository
from src.models import TeamModel

from .schemas import CreateTeam, UpdateTeam, PartialTeam


class TeamsRepository(SqlAlchemyRepository[TeamModel, CreateTeam, UpdateTeam, PartialTeam]):
    model = TeamModel
