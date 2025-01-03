# -*- coding: utf-8 -*-
from typing import Optional, Any
from collections import defaultdict
import math
from src.core.service import BaseService
from src.core.uow import UnitOfWork
from src.core.constants import DEFAULT_RATING, QUALIFICATION_COEFFICIENT
from src.models import RatingType, HistoryRatingLevel, RatingHistoryModel, MatchModel, CompetitionModel, \
    LeagueModel, TournametModel

from .schemas import CreateRatingHistory, CreateRating
from .repository import RatingRepository


def calculate_rating_correction():
    """Рассчитать величину поправки рейтинга игрока"""
    result = None

    return result


class HystoryStore:
    def __init__(self):
        self.__data = {}
        self.__competitions_history = defaultdict(list)

    def get_history(self, person_id: Any) -> Optional[RatingHistoryModel]:
        return self.__data.get(person_id)

    def set_history(self, person_id, obj: RatingHistoryModel):
        self.__data[person_id] = obj

    def add_history(self, competition_id: int, history: RatingHistoryModel):
        self.__competitions_history[competition_id].append(history)

    def competition_history(self, competition_id: int) -> list:
        return self.__competitions_history[competition_id]

    @property
    def data(self):
        return self.__data


class RatingService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository: RatingRepository = self.uow.ratings
        self.store = HystoryStore()

    async def calculate_rating(self, competition_id: Optional[int]) -> bool:
        competitions = await self.uow.competitions.all(order="date")
        for competition in competitions:
            tournament = competition.tournament
            league = tournament.league
            for match in competition.matches:
                await self.__calculate_match_rating(match, league, tournament)
            await self.__update_competition_rating(competition)
        await self.__update_rating()
        await self.uow.commit()
        return True

    async def __calculate_match_rating(self, match: MatchModel, league: LeagueModel, tournament: TournametModel):
        # Последние записи в истории рейтингов
        ft_first_p_history = self.store.get_history(match.first_team.first_player_id)
        ft_second_p_history = self.store.get_history(match.first_team.second_player_id)
        st_first_p_history = self.store.get_history(match.second_team.first_player_id)
        st_second_p_history = self.store.get_history(match.second_team.second_player_id)

        ft_first_p_rating = ft_first_p_history.rating if ft_first_p_history else DEFAULT_RATING
        ft_second_p_rating = None
        if match.first_team.second_player_id:
            ft_second_p_rating = ft_second_p_history.rating if ft_second_p_history else DEFAULT_RATING

        st_first_p_rating = st_first_p_history.rating if st_first_p_history else DEFAULT_RATING
        st_second_p_rating = None
        if match.second_team.second_player_id:
            st_second_p_rating = st_second_p_history.rating if st_second_p_history else DEFAULT_RATING

        coefficients = [1]
        if match.is_qualification:
            coefficients.append(QUALIFICATION_COEFFICIENT)

        ft_rating = self.__team_rating(list(filter(None, [ft_first_p_rating, ft_second_p_rating])))
        st_rating = self.__team_rating(list(filter(None, [st_first_p_rating, st_second_p_rating])))

        rating_diff = self.__calculate_rating_diff(
            match.first_team_score,
            match.second_team_score,
            ft_rating,
            st_rating,
            *coefficients
        )
        # Записи в историю
        ft_first_player_history = await self.uow.rating_history.update_or_create(CreateRatingHistory(
            league_id=league.id,
            tournament_id=tournament.id,
            type=RatingType.PLAYER,
            prev_history_id=ft_first_p_history.id if ft_first_p_history else None,
            level=HistoryRatingLevel.MATCH,
            player_id=match.first_team.first_player_id,
            competition_id=match.competition_id,
            match_id=match.id,
            diff=rating_diff,
            rating=ft_first_p_rating + rating_diff,
            matches_diff=1,
            matches=(ft_first_p_history.matches if ft_first_p_history else 0) + 1,
            wins=(ft_first_p_history.wins if ft_first_p_history else 0) + (
                1 if not match.is_draw and match.first_team_score > match.second_team_score else 0
            ),
            wins_diff=(
                1 if not match.is_draw and match.first_team_score > match.second_team_score else 0
            ),
            losses=(ft_first_p_history.losses if ft_first_p_history else 0) + (
                1 if not match.is_draw and match.first_team_score < match.second_team_score else 0
            ),
            losses_diff=(
                1 if not match.is_draw and match.first_team_score < match.second_team_score else 0
            )
        ), **{'level': HistoryRatingLevel.MATCH, 'player_id': match.first_team.first_player_id, 'match_id': match.id})
        self.store.set_history(match.first_team.first_player_id, ft_first_player_history)
        self.store.add_history(match.competition_id, ft_first_player_history)

        st_first_player_history = await self.uow.rating_history.update_or_create(CreateRatingHistory(
            league_id=league.id,
            tournament_id=tournament.id,
            type=RatingType.PLAYER,
            prev_history_id=st_first_p_history.id if st_first_p_history else None,
            level=HistoryRatingLevel.MATCH,
            player_id=match.second_team.first_player_id,
            competition_id=match.competition_id,
            match_id=match.id,
            diff=-rating_diff,
            rating=st_first_p_rating - rating_diff,
            matches_diff=1,

            matches=(st_first_p_history.matches if st_first_p_history else 0) + 1,
            wins=(st_first_p_history.wins if st_first_p_history else 0) + (
                1 if not match.is_draw and match.second_team_score > match.first_team_score else 0
            ),
            wins_diff=(
                1 if not match.is_draw and match.second_team_score > match.first_team_score else 0
            ),
            losses=(st_first_p_history.losses if st_first_p_history else 0) + (
                1 if not match.is_draw and match.second_team_score < match.first_team_score else 0
            ),
            losses_diff=(
                1 if not match.is_draw and match.second_team_score < match.first_team_score else 0
            ),
        ), **{'level': HistoryRatingLevel.MATCH, 'player_id': match.second_team.first_player_id, 'match_id': match.id})
        self.store.set_history(match.second_team.first_player_id, st_first_player_history)
        self.store.add_history(match.competition_id, st_first_player_history)

        if not match.is_singles:
            ft_second_player_history = await self.uow.rating_history.update_or_create(CreateRatingHistory(
                league_id=league.id,
                tournament_id=tournament.id,
                type=RatingType.PLAYER,
                prev_history_id=ft_second_p_history.id if ft_second_p_history else None,
                level=HistoryRatingLevel.MATCH,
                player_id=match.first_team.second_player_id,
                competition_id=match.competition_id,
                match_id=match.id,
                diff=rating_diff,
                rating=ft_second_p_rating + rating_diff,
                matches_diff=1,
                matches=(ft_second_p_history.matches if ft_second_p_history else 0) + 1,
                wins=(ft_second_p_history.wins if ft_second_p_history else 0) + (
                    1 if not match.is_draw and match.first_team_score > match.second_team_score else 0
                ),
                wins_diff=(
                    1 if not match.is_draw and match.first_team_score > match.second_team_score else 0
                ),
                losses=(ft_second_p_history.losses if ft_second_p_history else 0) + (
                    1 if not match.is_draw and match.first_team_score < match.second_team_score else 0
                ),
                losses_diff= (
                    1 if not match.is_draw and match.first_team_score < match.second_team_score else 0
                )
            ), **{'level': HistoryRatingLevel.MATCH, 'player_id': match.first_team.second_player_id, 'match_id': match.id})
            self.store.set_history(match.first_team.second_player_id, ft_second_player_history)
            self.store.add_history(match.competition_id, ft_second_player_history)

            st_second_player_history = await self.uow.rating_history.update_or_create(CreateRatingHistory(
                league_id=league.id,
                tournament_id=tournament.id,
                type=RatingType.PLAYER,
                prev_history_id=st_second_p_history.id if st_second_p_history else None,
                level=HistoryRatingLevel.MATCH,
                player_id=match.second_team.second_player_id,
                competition_id=match.competition_id,
                match_id=match.id,
                diff=-rating_diff,
                rating=st_second_p_rating - rating_diff,
                matches_diff=1,
                matches=(st_second_p_history.matches if st_second_p_history else 0) + 1,
                wins=(st_second_p_history.wins if st_second_p_history else 0) + (
                    1 if not match.is_draw and match.second_team_score > match.first_team_score else 0
                ),
                wins_diff= 1 if not match.is_draw and match.second_team_score > match.first_team_score else 0,
                losses=(st_second_p_history.losses if st_second_p_history else 0) + (
                    1 if not match.is_draw and match.second_team_score < match.first_team_score else 0
                ),
                losses_diff= 1 if not match.is_draw and match.second_team_score < match.first_team_score else 0,
            ), **{'level': HistoryRatingLevel.MATCH, 'player_id': match.second_team.second_player_id, 'match_id': match.id})
            self.store.set_history(match.second_team.second_player_id, st_second_player_history)
            self.store.add_history(match.competition_id, st_second_player_history)

    async def __update_rating(self):
        for player_id, rating_history in self.store.data.items():
            if not isinstance(player_id, int):
                continue
            last_history = self.store.get_history(('competition', player_id))

            await self.uow.ratings.update_or_create(CreateRating(
                type=RatingType.PLAYER,
                player_id=player_id,
                rating=rating_history.rating,
                matches=rating_history.matches,
                wins=rating_history.wins,
                losses=rating_history.losses,
                last_diff=last_history.diff if last_history else None
            ), **{'type': RatingType.PLAYER, 'player_id': player_id})

    async def __update_competition_rating(self, competition: CompetitionModel):
        tournament = competition.tournament
        league = tournament.league
        competition_ratings = self.store.competition_history(competition.id)
        players = {r.player_id for r in competition_ratings}
        history = dict()
        for player_id in players:
            last_history = self.store.get_history(('competition', player_id))
            history[player_id] = CreateRatingHistory(
                league_id=league.id,
                tournament_id=tournament.id,
                type=RatingType.PLAYER,
                prev_history_id=last_history.id if last_history else None,
                level=HistoryRatingLevel.COMPETITION,
                player_id=player_id,
                competition_id=competition.id,

                rating=DEFAULT_RATING,
                diff=0
            )

        for rating_history in competition_ratings:
            if rating_history.level == HistoryRatingLevel.COMPETITION:
                continue
            competition_history = history.get(rating_history.player_id)
            if not competition_history:
                continue
            competition_history.rating = rating_history.rating
            competition_history.matches = rating_history.matches
            competition_history.wins = rating_history.wins
            competition_history.losses = rating_history.losses
            competition_history.diff += rating_history.diff or 0
            competition_history.matches_diff += rating_history.matches_diff or 0
            competition_history.wins_diff += rating_history.wins_diff or 0
            competition_history.losses_diff += rating_history.losses_diff or 0

        for history_scheme in history.values():
            competition_history_model = await self.uow.rating_history.update_or_create(
                history_scheme,
                **{
                    'level': HistoryRatingLevel.COMPETITION,
                    'player_id': history_scheme.player_id,
                    'competition_id': competition.id
                })
            self.store.set_history(('competition', history_scheme.player_id), competition_history_model)

    @staticmethod
    def __team_rating(ratings: list):
        """Текущий рейтинг команды"""
        return int((2 * max(ratings) + min(ratings)) / 3)

    @staticmethod
    def __calculate_rating_diff(ft_score, st_score, ft_rating, st_rating, *coefficients):
        """Изменение рейтинга победителя"""
        winner_rating = ft_rating if ft_score > st_score else st_rating
        looser_rating = st_rating if ft_score > st_score else ft_rating
        w = 1 if ft_score > st_score else -1
        if ft_score == st_score:
            w = 1 if ft_rating < st_rating else -1
            winner_rating = min([st_rating, ft_rating])
            looser_rating = max([st_rating, ft_rating])
            if ft_rating == st_rating:
                w = 0

        k = math.fabs(ft_score - st_score) * 6
        if k < 0:
            k *= -1
        if k == 0:
            k = 3
        # n = 1 if winner_score > looser_score else 0.1
        n = 1

        result = w * k * (1 - (1 / (10 ** ((looser_rating - winner_rating) / 400) + 1))) * n
        if coefficients:
            for c in coefficients:
                result *= c
        return int(round(result))

    async def rating_list_with_count(self, limit: int, offset: int, search_string: Optional[str]):
        if search_string is not None:
            search_string = search_string.lower()
        count = await self.repository.rating_list_count(search_string)
        ratings = await self.repository.rating_list(limit, offset, search_string)
        return {'count': count, 'players': ratings}


class RatingHistoryService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = self.uow.rating_history

