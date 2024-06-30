from src.models import MatchModel, MatchSetModel

from .team import Team


class RatingMatch:
    """Расчет рейтинга в матче"""
    def __init__(self, competition, instance: MatchModel):
        self.competition = competition
        self.instance: MatchModel = instance
        self.first_team = Team(self, self.instance.first_team)
        self.second_team = Team(self, self.instance.second_team)

    @property
    def service(self):
        return self.competition.service

    @property
    def sets(self) -> list[MatchSetModel]:
        return self.instance.sets or []
