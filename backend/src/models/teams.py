from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.model import BaseModel

if TYPE_CHECKING:
    from .players import PlayerModel
    from .competitions import CompetitionModel


class TeamModel(BaseModel):
    """Команда"""
    __tablename__ = "teams"
    competition_order: Mapped[int] = mapped_column(Integer, nullable=True)
    # Соревнование
    competition_id: Mapped[int] = mapped_column(ForeignKey('competitions.id'), nullable=False)
    competition: Mapped["CompetitionModel"] = relationship(
        foreign_keys="TeamModel.competition_id",
        back_populates="teams"
    )
    # Игрок 1
    first_player_id: Mapped[int] = mapped_column(ForeignKey('players.id'), nullable=False)
    first_player: Mapped["PlayerModel"] = relationship(foreign_keys="TeamModel.first_player_id", lazy='joined')
    # Игрок 2
    second_player_id: Mapped[int] = mapped_column(ForeignKey('players.id'), nullable=True)
    second_player: Mapped["PlayerModel"] = relationship(foreign_keys="TeamModel.second_player_id", lazy='joined')

    def __str__(self):
        name = f'TeamModel: {self.id} '
        name += str(self.first_player)
        if self.second_player_id:
            name += f'/{str(self.second_player)}'
        return name

    @property
    def is_single_player(self) -> bool:
        return self.second_player_id is None

    @property
    def players(self) -> list['PlayerModel']:
        if self.second_player:
            return [self.first_player, self.second_player]
        return [self.first_player]
