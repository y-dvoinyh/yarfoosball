from typing import Optional, Sequence
from sqlalchemy import select, func, or_
from src.core.repository import SqlAlchemyRepository
from src.models import RatingModel, RatingHistoryModel, PlayerModel, RatingType

from .schemas import (
    CreateRating,
    UpdateRating,
    PartialRating,
    CreateRatingHistory,
    UpdateRatingHistory,
    PartialRatingHistory
)


class RatingRepository(
    SqlAlchemyRepository[RatingModel, CreateRating, UpdateRating, PartialRating]
):
    model = RatingModel

    async def rating_list(self, limit: int, offset: int, search_string: Optional[str]) -> Sequence:
        rating_subquery = (
            select(
                func.row_number().over(
                    order_by=[self.model.rating.desc(), self.model.id]
                ).label('number'),
                self.model.player_id,
                self.model.rating,
                self.model.matches,
                self.model.wins,
                self.model.losses,
                self.model.last_diff
            )
            .where(self.model.type == RatingType.PLAYER)
            .order_by(self.model.rating.desc(), self.model.id)
            .subquery()
        )

        rating = rating_subquery.c

        stmt = (
            select(
                rating.player_id,
                PlayerModel.id,
                func.concat_ws(' ', PlayerModel.first_name, PlayerModel.last_name).label('full_name'),
                rating.number,
                rating.rating,
                rating.matches,
                rating.wins,
                rating.losses,
                rating.last_diff
            )
            .select_from(PlayerModel)
            .join(rating_subquery, rating.player_id == PlayerModel.id, isouter=True)

            .order_by(rating.number)
            .limit(limit)
            .offset(offset)
        )
        stmt = self.__list_where(stmt, search_string)
        result = await self._session.execute(stmt)
        return result.all()

    async def rating_list_count(self, search_string: Optional[str]) -> int:
        stmt = select(func.count(PlayerModel.id))
        stmt = self.__list_where(stmt, search_string)
        result = await self._session.execute(stmt)
        count = result.scalar()
        return count

    @staticmethod
    def __list_where(query, search_string):
        if search_string:
            query = query.where(
                or_(
                    func.lower(PlayerModel.first_name).ilike(f"%{search_string}%"),
                    func.lower(PlayerModel.last_name).ilike(f"%{search_string}%"),
                    func.lower(func.concat_ws(
                        ' ', PlayerModel.last_name, PlayerModel.first_name)).ilike(f"%{search_string}%"),
                    func.lower(func.concat_ws(
                        ' ', PlayerModel.first_name, PlayerModel.last_name)).ilike(f"%{search_string}%")
                )
            )
        return query


class RatingHistoryRepository(
    SqlAlchemyRepository[RatingHistoryModel, CreateRatingHistory, UpdateRatingHistory, PartialRatingHistory]
):
    model = RatingHistoryModel
