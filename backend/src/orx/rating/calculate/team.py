from src.models import TeamModel

from .player import Player


class Team:
    """Расчет рейтинга в матче"""
    def __init__(self, match, instance: TeamModel):
        self.match = match
        self.instance: TeamModel = instance
        self.players: list[Player] = [Player(self, self.instance.first_player)]
        if self.instance.second_player_id:
            self.players.append(Player(self, self.instance.second_player))

    @property
    def service(self):
        return self.match.service

    @property
    async def rating(self) -> int:
        ratings = []
        for player in self.players:
            rating = await player.rating
            ratings.append(rating)
        return (2*max(ratings) + min(ratings)) / 3
