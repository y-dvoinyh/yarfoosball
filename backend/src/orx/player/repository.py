from src.core.repository import SqlAlchemyRepository
from src.models import PlayerModel

from .schemas import CreatePlayer, UpdatePlayer, PartialPlayer


class PlayersRepository(SqlAlchemyRepository[PlayerModel, CreatePlayer, UpdatePlayer, PartialPlayer]):
    model = PlayerModel
