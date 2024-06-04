from src.core.repository import SqlAlchemyRepository
from src.models.players import PlayerModel

from .schemas import CreatePlayer, UpdatePlayer, PartialPlayer


class PlayersRepository(SqlAlchemyRepository[PlayerModel, CreatePlayer, UpdatePlayer, PartialPlayer]):
    model = PlayerModel
