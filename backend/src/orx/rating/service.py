from typing import Optional
import math
from src.core.service import BaseService
from src.core.constants import DEFAULT_RATING
from src.models import RatingType, HistoryRatingLevel, RatingHistoryModel, MatchModel, TeamModel

from .schemas import CreateRatingHistory, CreateRating
from .repository import RatingRepository


class HystoryStore:
    def __init__(self):
        self.__data = {}

    def get_history(self, person_id: int) -> Optional[RatingHistoryModel]:
        return self.__data.get(person_id)

    def set_history(self, person_id, obj: RatingHistoryModel):
        self.__data[person_id] = obj

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
            print(competition.tournament.league_id)
            for match in competition.matches:
                await self.__calculate_match_rating(match)
            await self.__update_rating()
        await self.uow.commit()
        return True

    async def __calculate_match_rating(self, match: MatchModel):

        # Последние записи в истории рейтингов
        winner_first_p_history = self.store.get_history(match.winner.first_player_id)
        winner_second_p_history = self.store.get_history(match.winner.second_player_id)
        looser_first_p_history = self.store.get_history(match.looser.first_player_id)
        looser_second_p_history = self.store.get_history(match.looser.second_player_id)

        winner_first_p_rating = winner_first_p_history.rating if winner_first_p_history else DEFAULT_RATING
        winner_second_p_rating = None
        if match.winner.second_player_id:
            winner_second_p_rating = winner_second_p_history.rating if winner_second_p_history else DEFAULT_RATING

        looser_first_p_rating = looser_first_p_history.rating if looser_first_p_history else DEFAULT_RATING
        looser_second_p_rating = None
        if match.looser.second_player_id:
            looser_second_p_rating = looser_second_p_history.rating if looser_second_p_history else DEFAULT_RATING

        rating_diff = self.__calculate_rating_diff(
            match.winner_score,
            match.looser_score,
            self.__team_rating(list(filter(None, [winner_first_p_rating, winner_second_p_rating]))),
            self.__team_rating(list(filter(None, [looser_first_p_rating, looser_second_p_rating])))
        )

        # Записи в историю
        winner_first_player_history = await self.uow.rating_history.update_or_create(CreateRatingHistory(
            type=RatingType.PLAYER,
            prev_history_id=winner_first_p_history.id if winner_first_p_history else None,
            level=HistoryRatingLevel.MATCH,
            player_id=match.winner.first_player_id,
            match_id=match.id,
            diff=rating_diff,
            rating=winner_first_p_rating + rating_diff
        ), **{'level': HistoryRatingLevel.MATCH, 'player_id': match.winner.first_player_id, 'match_id': match.id})
        self.store.set_history(match.winner.first_player_id, winner_first_player_history)

        looser_first_player_history = await self.uow.rating_history.update_or_create(CreateRatingHistory(
            type=RatingType.PLAYER,
            prev_history_id=looser_first_p_history.id if looser_first_p_history else None,
            level=HistoryRatingLevel.MATCH,
            player_id=match.looser.first_player_id,
            match_id=match.id,
            diff=-1 * rating_diff,
            rating=looser_first_p_rating - rating_diff
        ), **{'level': HistoryRatingLevel.MATCH, 'player_id': match.looser.first_player_id, 'match_id': match.id})
        self.store.set_history(match.looser.first_player_id, looser_first_player_history)

        if not match.is_singles:
            winner_second_player_history = await self.uow.rating_history.update_or_create(CreateRatingHistory(
                type=RatingType.PLAYER,
                prev_history_id=winner_second_p_history.id if winner_second_p_history else None,
                level=HistoryRatingLevel.MATCH,
                player_id=match.winner.second_player_id,
                match_id=match.id,
                diff=rating_diff,
                rating=winner_second_p_rating + rating_diff
            ), **{'level': HistoryRatingLevel.MATCH, 'player_id': match.winner.second_player_id, 'match_id': match.id})
            self.store.set_history(match.winner.second_player_id, winner_second_player_history)

            looser_second_player_history = await self.uow.rating_history.update_or_create(CreateRatingHistory(
                type=RatingType.PLAYER,
                prev_history_id=looser_second_p_history.id if looser_second_p_history else None,
                level=HistoryRatingLevel.MATCH,
                player_id=match.looser.second_player_id,
                match_id=match.id,
                diff=(-1 * rating_diff),
                rating=looser_second_p_rating - rating_diff
            ), **{'level': HistoryRatingLevel.MATCH, 'player_id': match.looser.second_player_id, 'match_id': match.id})
            self.store.set_history(match.looser.second_player_id, looser_second_player_history)

    async def __update_rating(self):
        for player_id, rating_history in self.store.data.items():
            await self.uow.ratings.update_or_create(CreateRating(
                type=RatingType.PLAYER,
                player_id=player_id,
                rating=rating_history.rating
            ), **{'type': RatingType.PLAYER, 'player_id': player_id})

    @staticmethod
    def __team_rating(ratings: list):
        """Текущий рейтинг команды"""
        return int((2 * max(ratings) + min(ratings)) / 3)

    @staticmethod
    def __calculate_rating_diff(winner_score, looser_score, winner_rating, looser_rating):
        """Изменение рейтинга победителя"""
        w = 1 if winner_score > looser_score else -1
        k = math.fabs(winner_score - looser_score) * 6
        n = 1 if winner_score > looser_score else 0.1
        return int(w * k * (1 - (1 / (10 ** ((looser_rating - winner_rating) / 400) + 1))) * n)

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

