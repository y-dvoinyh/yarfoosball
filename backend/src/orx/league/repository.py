from src.core.repository import SqlAlchemyRepository
from src.models.leagues import LeagueModel

from .schemas import CreateLeague, UpdateLeague, PartialLeague


class LeaguesRepository(SqlAlchemyRepository[LeagueModel, CreateLeague, UpdateLeague, PartialLeague]):
    model = LeagueModel
