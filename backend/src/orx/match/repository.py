from src.core.repository import SqlAlchemyRepository
from src.models import MatchModel, MatchSetModel

from .schemas import CreateMatch, UpdateMatch, PartialMatch, CreateSet, UpdateSet, PartialSet


class MatchsRepository(SqlAlchemyRepository[MatchModel, CreateMatch, UpdateMatch, PartialMatch]):
    model = MatchModel


class SetRepository(SqlAlchemyRepository[MatchSetModel, CreateSet, UpdateSet, PartialSet]):
    model = MatchSetModel
