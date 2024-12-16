from typing import Optional, Sequence
from src.core.repository import SqlAlchemyRepository
from src.models import PlayerModel, RatingHistoryModel, CompetitionModel, RatingModel

from sqlalchemy import select, func, and_

from .schemas import CreatePlayer, UpdatePlayer, PartialPlayer


class PlayersRepository(SqlAlchemyRepository[PlayerModel, CreatePlayer, UpdatePlayer, PartialPlayer]):
    model = PlayerModel

    async def competitions_list_count(self, player_id: int, search_string: Optional[str]):
        stmt = select(func.count(RatingHistoryModel.id))
        stmt = self.__list_where(stmt, player_id, search_string)
        result = await self._session.execute(stmt)
        count = result.scalar()
        return count

    async def competitions_list(self, player_id: int, limit: int, offset: int, search_string: Optional[str]) -> Sequence:

        rating_subquery = (
            select(
                RatingHistoryModel.competition_id,
                RatingHistoryModel.rating,
                RatingHistoryModel.diff,
                RatingHistoryModel.matches_diff,
                RatingHistoryModel.wins_diff,
                RatingHistoryModel.losses_diff
            )
            .where(and_(
                RatingHistoryModel.level == 'COMPETITION',
                RatingHistoryModel.type == 'PLAYER',
                RatingHistoryModel.player_id == player_id
            ))
            .subquery()
        )

        rating = rating_subquery.c

        stmt = (
            select(
                CompetitionModel.id,
                CompetitionModel.name,
                CompetitionModel.date,
                rating.rating,
                rating.diff,
                rating.matches_diff,
                rating.wins_diff,
                rating.losses_diff
            )
            .select_from(CompetitionModel)
            .join(rating_subquery, rating.competition_id == CompetitionModel.id)

            .order_by(CompetitionModel.date.desc())
            .limit(limit)
            .offset(offset)
        )
        # stmt = self.__list_where(stmt, player_id, search_string)
        result = await self._session.execute(stmt)
        return result.all()

    @staticmethod
    def __list_where(query, player_id, search_string):
        query = query.where(
            and_(
                RatingHistoryModel.level == 'COMPETITION',
                RatingHistoryModel.type == 'PLAYER',
                RatingHistoryModel.player_id == player_id
            )
        )
        return query

    async def get_player_info(self, player_id: int):
        stmt = select(
            RatingModel.rating,
            RatingModel.matches,
            RatingModel.wins,
            RatingModel.losses,

            PlayerModel.first_name,
            PlayerModel.last_name,
        ).join(PlayerModel, PlayerModel.id == RatingModel.player_id).where(
            and_(
                RatingModel.player_id == player_id,
                RatingModel.type == 'PLAYER'
            )
        )
        row = await self._session.execute(stmt)
        return row.first()
