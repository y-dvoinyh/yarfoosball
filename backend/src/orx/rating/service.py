# -*- coding: utf-8 -*-
from typing import Optional, Any
from collections import defaultdict
import math
from src.core.service import BaseService
from src.core.constants import DEFAULT_RATING, QUALIFICATION_COEFFICIENT, K_SINGLE_COEFFICIENT, K_BEST_OF_3_COEFFICIENT
from src.models import RatingType, HistoryRatingLevel, RatingHistoryModel, MatchModel, CompetitionModel, \
    LeagueModel, TournametModel, Rank

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

    @staticmethod
    def get_rank(cerrent_rank, rating):
        if not rating:
            return Rank.beginner

        if rating >= 2000 or (cerrent_rank == Rank.master and rating >= 1900):
            return Rank.master
        if rating >= 1750 or (cerrent_rank == Rank.pro and rating >= 1650):
            return Rank.pro
        if rating >= 1500 or (cerrent_rank == Rank.semipro and rating >= 1400):
            return Rank.semipro
        if rating >= 1250 or (cerrent_rank == Rank.amateur and rating >= 1150):
            return Rank.amateur
        if rating >= 1000 or (cerrent_rank == Rank.novice and rating >= 900):
            return Rank.novice

        if rating < 1000:
            return Rank.beginner

        return Rank.beginner

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
            match.is_single_set,
            ft_rating,
            st_rating,
            *coefficients
        )

        # Учет коэффициента достоверности
        (
            ft_first_player_rating_diff,
            st_first_player_rating_diff,
            ft_second_player_rating_diff,
            st_second_player_rating_diff
        ) = [rating_diff] * 4

        (
            ft_first_player_d,
            st_first_player_d,
            ft_second_player_d,
            st_second_player_d
        ) = [1] * 4

        def __is_actual(p_h):
            return p_h and p_h.matches and p_h.matches > 10

        ft_first_player_is_actual = __is_actual(ft_first_p_history)
        st_first_player_is_actual = __is_actual(st_first_p_history)
        ft_second_player_is_actual = __is_actual(ft_second_p_history)
        st_second_player_is_actual = __is_actual(st_second_p_history)

        if match.is_singles:
            # Если рейтинг участника до матча был предварительным, а рейтинг его
            # противника – актуальным, D = 2 .
            if ft_first_player_is_actual != st_first_player_is_actual:
                ft_first_player_d = 0.5 if ft_first_player_is_actual else 2
                st_first_player_d = 0.5 if st_first_player_is_actual else 2
        else:
            # Если рейтинг участника до матча был предварительным, а рейтинги обоих
            # его противников – актуальными, D = 2.

            # Если рейтинг участника до матча был актуальным, а рейтинг хотя бы одного
            # другого участника матча (в том числе его партнера) – предварительным,
            # D = 0,5 .

            # первый игрок первой команды
            if not ft_first_player_is_actual and st_first_player_is_actual and st_second_player_is_actual:
                ft_first_player_d = 2
            elif ft_first_player_is_actual and (
                    not st_first_player_is_actual or not ft_second_player_is_actual or not st_second_player_is_actual):
                ft_first_player_d = 0.5
            # второй игрок первой команды
            if not ft_second_player_is_actual and st_first_player_is_actual and st_second_player_is_actual:
                ft_second_player_d = 2
            elif ft_second_player_is_actual and (
                    not st_first_player_is_actual or not ft_first_player_is_actual or not st_second_player_is_actual):
                ft_second_player_d = 0.5
            # первый игрок второй команды
            if not st_first_player_is_actual and ft_first_player_is_actual and ft_second_player_is_actual:
                st_first_player_d = 2
            elif st_first_player_is_actual and (
                    not ft_second_player_is_actual or not ft_first_player_is_actual or not st_second_player_is_actual):
                st_first_player_d = 0.5
            # второй игрок второй команды
            if not st_second_player_is_actual and ft_first_player_is_actual and ft_second_player_is_actual:
                st_second_player_d = 2
            elif st_second_player_is_actual and (
                    not ft_second_player_is_actual or not ft_first_player_is_actual or not st_first_player_is_actual):
                st_second_player_d = 0.5

        ft_first_player_rating_diff = int(round(ft_first_player_rating_diff * ft_first_player_d))
        st_first_player_rating_diff = int(round(st_first_player_rating_diff * st_first_player_d))
        ft_second_player_rating_diff = int(round(ft_second_player_rating_diff * ft_second_player_d))
        st_second_player_rating_diff = int(round(st_second_player_rating_diff * st_second_player_d))

        ft_first_player_new_rating = ft_first_p_rating + ft_first_player_rating_diff
        st_first_player_new_rating = st_first_p_rating - st_first_player_rating_diff

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
            diff=ft_first_player_rating_diff,
            rating=ft_first_player_new_rating,
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
            ),
            goals=(ft_first_p_history.goals if ft_first_p_history else 0) + match.first_team_goals,
            goals_diff=match.first_team_goals,
            rank=self.get_rank((ft_first_p_history.rank if ft_first_p_history else None), ft_first_player_new_rating)
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
            diff=-st_first_player_rating_diff,
            rating=st_first_player_new_rating,
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
            goals=(st_first_p_history.goals if st_first_p_history else 0) + match.second_team_goals,
            goals_diff=match.second_team_goals,
            rank=self.get_rank((st_first_p_history.rank if st_first_p_history else None), st_first_player_new_rating)
        ), **{'level': HistoryRatingLevel.MATCH, 'player_id': match.second_team.first_player_id, 'match_id': match.id})
        self.store.set_history(match.second_team.first_player_id, st_first_player_history)
        self.store.add_history(match.competition_id, st_first_player_history)

        if not match.is_singles:
            ft_second_player_new_rating = ft_second_p_rating + ft_second_player_rating_diff
            st_second_player_new_rating = st_second_p_rating - st_second_player_rating_diff

            ft_second_player_history = await self.uow.rating_history.update_or_create(CreateRatingHistory(
                league_id=league.id,
                tournament_id=tournament.id,
                type=RatingType.PLAYER,
                prev_history_id=ft_second_p_history.id if ft_second_p_history else None,
                level=HistoryRatingLevel.MATCH,
                player_id=match.first_team.second_player_id,
                competition_id=match.competition_id,
                match_id=match.id,
                diff=ft_second_player_rating_diff,
                rating=ft_second_player_new_rating,
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
                losses_diff=(
                    1 if not match.is_draw and match.first_team_score < match.second_team_score else 0
                ),
                goals=(ft_second_p_history.goals if ft_second_p_history else 0) + match.first_team_goals,
                goals_diff=match.first_team_goals,
                rank=self.get_rank((ft_second_p_history.rank if ft_second_p_history else None), ft_second_player_new_rating)
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
                diff=-st_second_player_rating_diff,
                rating=st_second_player_new_rating,
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
                goals=(st_second_p_history.goals if st_second_p_history else 0) + match.second_team_goals,
                goals_diff=match.second_team_goals,
                rank=self.get_rank((st_second_p_history.rank if st_second_p_history else None),
                                   st_second_player_new_rating)
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
                goals=rating_history.goals,
                last_diff=last_history.diff if last_history else None,
                tournaments=last_history.tournaments,
                rank=last_history.rank
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
                diff=0,
                tournaments=(last_history.tournaments + 1) if last_history else 1
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
            competition_history.goals = rating_history.goals
            competition_history.diff += rating_history.diff or 0
            competition_history.matches_diff += rating_history.matches_diff or 0
            competition_history.wins_diff += rating_history.wins_diff or 0
            competition_history.losses_diff += rating_history.losses_diff or 0
            competition_history.goals_diff += rating_history.goals_diff or 0
            competition_history.rank = rating_history.rank

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
    def __calculate_rating_diff(ft_score, st_score, is_single_set, ft_rating, st_rating, *coefficients):
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

        if is_single_set:
            k = math.fabs(ft_score - st_score) * K_SINGLE_COEFFICIENT
            if k < 0:
                k *= -1
            if k == 0:
                k = 3
        else:
            k = (max(ft_score, st_score) - min(ft_score, st_score)) * K_BEST_OF_3_COEFFICIENT
        n = 1

        result = w * k * (1 - (1 / (10 ** ((looser_rating - winner_rating) / 400) + 1))) * n
        if coefficients:
            for c in coefficients:
                result *= c
        return result

    async def rating_list_with_count(self, limit: int, offset: int, search_string: Optional[str], sort_by, desc):
        if search_string is not None:
            search_string = search_string.lower()
        count = await self.repository.rating_list_count(search_string)
        ratings = await self.repository.rating_list(limit, offset, search_string, sort_by, desc)
        return {'count': count, 'players': ratings}


class RatingHistoryService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = self.uow.rating_history

