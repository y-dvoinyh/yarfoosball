from typing import Optional, Sequence
from src.core.repository import SqlAlchemyRepository
from src.models import PlayerModel, RatingHistoryModel, CompetitionModel, RatingModel, MatchModel, MatchSetModel, TeamModel, Rank

from sqlalchemy import select, func, and_, String, literal_column, case, union_all, Float, Integer
from sqlalchemy.orm import aliased

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
                RatingHistoryModel.losses_diff,
                RatingHistoryModel.goals_diff
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
                rating.losses_diff,
                rating.goals_diff
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

    async def player_competition(self, player_id: int, competition_id: int):

        ft = aliased(TeamModel)
        st = aliased(TeamModel)
        ffp = aliased(PlayerModel)
        fsp = aliased(PlayerModel)
        sfp = aliased(PlayerModel)
        ssp = aliased(PlayerModel)

        match_sets_subquery = select(
            func.array_to_string(
                func.array_agg(
                    func.concat_ws(
                        ':',
                        MatchSetModel.first_team_score.cast(String),
                        MatchSetModel.second_team_score.cast(String))),
                literal_column("' - '")
            ).label('score')
        ).where(
            MatchSetModel.match_id == MatchModel.id
        ).group_by(
            MatchSetModel.match_id
        ).lateral()

        query = (
            select(
                MatchModel.id,
                MatchModel.is_qualification,
                RatingHistoryModel.rating,
                RatingHistoryModel.diff,
                RatingHistoryModel.wins_diff,
                RatingHistoryModel.losses_diff,
                RatingHistoryModel.goals_diff,
                match_sets_subquery.c.score,
                case(
                    (RatingHistoryModel.wins_diff > 0, 'green'),
                    (RatingHistoryModel.losses_diff > 0, 'red'),
                    else_=None
                ).label('color'),
                ffp.id.label('left_team_first_id'),
                func.concat(ffp.first_name, ' ', ffp.last_name).label('left_team_first'),
                fsp.id.label('left_team_second_id'),
                func.concat(fsp.first_name, ' ', fsp.last_name).label('left_team_second'),
                sfp.id.label('right_team_first_id'),
                func.concat(sfp.first_name, ' ', sfp.last_name).label('right_team_first'),
                ssp.id.label('right_second_id'),
                func.concat(ssp.first_name, ' ', ssp.last_name).label('right_second'),
            )
            .select_from(RatingHistoryModel)
            .join(MatchModel, MatchModel.id == RatingHistoryModel.match_id)
            .join(ft, ft.id == MatchModel.first_team_id)
            .join(ffp, ffp.id == ft.first_player_id)
            .join(fsp, fsp.id == ft.second_player_id, isouter=True)
            .join(st, st.id == MatchModel.second_team_id)
            .join(sfp, sfp.id == st.first_player_id)
            .join(ssp, ssp.id == st.second_player_id, isouter=True)
            .join(
                match_sets_subquery,
                literal_column('TRUE')
            )
            .where(
                RatingHistoryModel.player_id == player_id,
                RatingHistoryModel.level == 'MATCH',
                RatingHistoryModel.type == 'PLAYER',
                RatingHistoryModel.competition_id == competition_id
            )
            .order_by(MatchModel.order)
        )
        result = await self._session.execute(query)
        return result.all()

    async def get_partners(self, player_id: int):
        partners = select(
            (RatingHistoryModel.wins_diff > 0).label('is_win'),
            (RatingHistoryModel.losses_diff > 0).label('is_losse'),
            case(
               (RatingHistoryModel.player_id == TeamModel.first_player_id, TeamModel.second_player_id),
                else_=TeamModel.first_player_id
            ).label('id')
        ).select_from(RatingHistoryModel)\
            .join(MatchModel, MatchModel.id == RatingHistoryModel.match_id) \
            .join(TeamModel, and_(
                TeamModel.id.in_([MatchModel.first_team_id, MatchModel.second_team_id]),
                RatingHistoryModel.player_id.in_([TeamModel.first_player_id, TeamModel.second_player_id])
            )) \
            .where(
                RatingHistoryModel.player_id == player_id,
                RatingHistoryModel.level == 'MATCH',
                RatingHistoryModel.type == 'PLAYER',
                TeamModel.second_player_id.isnot(None)
            ).subquery()

        groupped_wins = select(
            partners.c.id,
            partners.c.is_win,
            partners.c.is_losse,
            func.count().label('count')
        ).where(partners.c.is_win.is_(True)) \
            .group_by(partners.c.id, partners.c.is_win, partners.c.is_losse) \
            .order_by(func.count().desc(), partners.c.id) \
            .limit(3)

        groupped_losses = select(
            partners.c.id,
            partners.c.is_win,
            partners.c.is_losse,
            func.count().label('count')
        ).where(partners.c.is_losse.is_(True)) \
            .group_by(partners.c.id, partners.c.is_win, partners.c.is_losse) \
            .order_by(func.count().desc(), partners.c.id) \
            .limit(3)

        limited = union_all(groupped_wins, groupped_losses)

        final_query = select(
            PlayerModel.id,
            limited.c.is_win,
            limited.c.is_losse,
            limited.c.count,
            func.concat(PlayerModel.first_name, ' ', PlayerModel.last_name).label('name')
        ).outerjoin(PlayerModel, PlayerModel.id == limited.c.id) \
            .order_by(limited.c.is_win.desc(), limited.c.count.desc())
        result = await self._session.execute(final_query)
        return result.all()

    async def get_opponents(self, player_id: int):
        opponents = select(
            PlayerModel.id,
            (RatingHistoryModel.wins_diff > 0).label('is_win'),
            (RatingHistoryModel.losses_diff > 0).label('is_losse'),
        ).select_from(RatingHistoryModel) \
            .join(MatchModel, MatchModel.id == RatingHistoryModel.match_id) \
            .join(
                TeamModel,
                and_(
                    TeamModel.id.in_([MatchModel.first_team_id, MatchModel.second_team_id]),
                    RatingHistoryModel.player_id.not_in([TeamModel.first_player_id, TeamModel.second_player_id])
                )
            ) \
            .join(PlayerModel, PlayerModel.id.in_([TeamModel.first_player_id, TeamModel.second_player_id])) \
            .where(
                RatingHistoryModel.player_id == player_id,
                RatingHistoryModel.level == 'MATCH',
                RatingHistoryModel.type == 'PLAYER'
            ).subquery()

        groupped_wins = select(
            opponents.c.id,
            opponents.c.is_win,
            opponents.c.is_losse,
            func.count().label('count')
        ).where(opponents.c.is_win.is_(True)) \
            .group_by(opponents.c.id, opponents.c.is_win, opponents.c.is_losse) \
            .order_by(func.count().desc(), opponents.c.id) \
            .limit(3)

        groupped_losses = select(
            opponents.c.id,
            opponents.c.is_win,
            opponents.c.is_losse,
            func.count().label('count')
        ).where(opponents.c.is_losse.is_(True)) \
            .group_by(opponents.c.id, opponents.c.is_win, opponents.c.is_losse) \
            .order_by(func.count().desc(), opponents.c.id) \
            .limit(3)

        limited = union_all(groupped_wins, groupped_losses)

        final_query = select(
            PlayerModel.id,
            limited.c.is_win,
            limited.c.is_losse,
            limited.c.count,
            func.concat(PlayerModel.first_name, ' ', PlayerModel.last_name).label('name')
        ).outerjoin(PlayerModel, PlayerModel.id == limited.c.id) \
            .order_by(limited.c.is_win.desc(), limited.c.count.desc())
        result = await self._session.execute(final_query)
        return result.all()

    async def get_player_statictic(self, player_id: int):
        # Подзапрос для статистики
        statistic = select(
            RatingHistoryModel.player_id,
            func.count().label('competitions_count'),
            func.count().filter(RatingHistoryModel.place == 1).label('gold'),
            func.count().filter(RatingHistoryModel.place == 2).label('silver'),
            func.count().filter(RatingHistoryModel.place == 3).label('bronze')
        ).select_from(RatingHistoryModel).where(
            RatingHistoryModel.player_id == player_id,
            RatingHistoryModel.type == 'PLAYER',
            RatingHistoryModel.level == 'COMPETITION'
        ).group_by(RatingHistoryModel.player_id).alias('statistic')

        # Основной запрос
        query = select(
            PlayerModel.id,
            func.concat(PlayerModel.first_name, ' ', PlayerModel.last_name).label('name'),
            RatingModel.rating,
            RatingModel.matches,
            RatingModel.wins,
            RatingModel.losses,
            RatingModel.rank,
            case(
                (RatingModel.rank == Rank.beginner, 'grey'),
                (RatingModel.rank == Rank.novice, 'blue'),
                (RatingModel.rank == Rank.amateur, 'green'),
                (RatingModel.rank == Rank.semipro, 'light-blue'),
                (RatingModel.rank == Rank.pro, 'amber'),
                (RatingModel.rank == Rank.master, 'red'),
            ).label('color'),
            case((RatingModel.wins > 0,
                  (RatingModel.wins.cast(Float) / RatingModel.matches.cast(Float) * 100).cast(Integer)),
                 else_=0).label('percent_wins'),
            (RatingModel.matches - (RatingModel.wins + RatingModel.losses)).label('draws'),
            statistic.c.competitions_count,
            statistic.c.gold,
            statistic.c.silver,
            statistic.c.bronze
        ).select_from(PlayerModel)\
            .outerjoin(statistic, statistic.c.player_id == PlayerModel.id) \
            .outerjoin(RatingModel, and_((RatingModel.player_id == PlayerModel.id), (RatingModel.type == 'PLAYER'))) \
            .where(PlayerModel.id == player_id)
        row = await self._session.execute(query)
        return row.first()

    async def get_series(self, player_id: int):
        # Используем SQLAlchemy для составления запроса
        competition_alias = aliased(CompetitionModel)
        match_alias = aliased(MatchModel)

        query = (
            select(
                func.row_number().over().label('order_num'),
                RatingHistoryModel.wins_diff,
                RatingHistoryModel.losses_diff
            )
            .select_from(RatingHistoryModel)
            .outerjoin(competition_alias, competition_alias.id == RatingHistoryModel.competition_id)
            .outerjoin(match_alias, match_alias.id == RatingHistoryModel.match_id)
            .filter(
                RatingHistoryModel.player_id == player_id,
                RatingHistoryModel.type == 'PLAYER',
                RatingHistoryModel.level == 'MATCH'
            )
            .order_by(competition_alias.date, match_alias.order)
        )

        result = await self._session.execute(query)

        max_wins = 0
        max_loss = 0
        max_draws = 0
        draws = 0
        wins = 0
        loss = 0

        for row in result:

            if row.wins_diff:
                loss = 0
                draws = 0
                wins += 1
                if wins > max_wins:
                    max_wins = wins
            elif row.losses_diff:
                wins = 0
                draws = 0
                loss += 1
                if loss > max_loss:
                    max_loss = loss
            else:
                loss = 0
                wins = 0

                draws += 1
                if draws > max_draws:
                    max_draws = draws

        return {
            's_wins': max_wins,
            's_loss': max_loss,
            's_draws': max_draws
        }
