from typing import Optional, Sequence
from sqlalchemy import select, func, or_, case
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

    async def rating_list(self, limit: int, offset: int, search_string: Optional[str], sort_by, desc) -> Sequence:
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
                self.model.last_diff,
                self.model.goals,
                self.model.tournaments,
                case(
                    (self.model.matches > 0, (100*((self.model.wins or 0) / (self.model.matches or 1)))),
                    else_=0
                ).label('percent'),

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
                rating.last_diff,
                rating.goals,
                rating.tournaments
            )
            .select_from(PlayerModel)
            .join(rating_subquery, rating.player_id == PlayerModel.id, isouter=True)
            .limit(limit)
            .offset(offset)
        )
        stmt = self.__list_where(stmt, search_string)

        order_by_first = rating.number if desc else rating.number.desc()

        if sort_by == 'matches':
            order_by_first = rating.matches.desc() if desc else rating.matches
        elif sort_by == 'goals':
            order_by_first = rating.goals.desc() if desc else rating.goals
        elif sort_by == 'wins':
            order_by_first = rating.wins.desc() if desc else rating.wins
        elif sort_by == 'losses':
            order_by_first = rating.losses.desc() if desc else rating.losses
        elif sort_by == 'percent_win':
            order_by_first = rating.percent.desc() if desc else rating.percent
        elif sort_by == 'tournaments':
            order_by_first = rating.tournaments.desc() if desc else rating.tournaments

        stmt = stmt.order_by(order_by_first, rating.player_id)

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
