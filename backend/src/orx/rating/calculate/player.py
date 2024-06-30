from src.models import PlayerModel, RatingType

from ..schemas import CreateRatingHistory, HistoryRatingLevel
from .service import RatingService


class Player:
    def __init__(self, team, instance: PlayerModel):
        self.team = team
        self.instance: PlayerModel = instance
        self.match_history = []
        self.competition_history = []
        self.__match_rating_history = None
        self.__competition_rating_history = None

    @property
    def service(self) -> RatingService:
        return self.team.service

    @property
    async def match_rating_history(self):
        if self.__match_rating_history is None:
            __filter = {
                'type': RatingType.PLAYER,
                'level': HistoryRatingLevel.MATCH,
                'player_id': self.instance.id,
                'league_id': None,
                'tournament_id': None,
                'competition_id': None,
                'prev_history_id': None,
                'match_id': None
            }
            self.match_rating_history = await self.service.get_rating_history(**__filter)
            if self.__match_rating_history is None:
                self.match_rating_history = await self.service.create_rating_history(CreateRatingHistory(
                    **__filter
                ))
        return self.__match_rating_history

    @match_rating_history.setter
    def match_rating_history(self, data):
        self.match_history.append(self.match_rating_history)
        self.__match_rating_history = data

    @property
    async def rating(self):
        match_rating_history = await self.match_rating_history
        return match_rating_history.rating
