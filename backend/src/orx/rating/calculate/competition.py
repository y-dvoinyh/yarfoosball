
from src.models import CompetitionModel
from .match import RatingMatch


class RatingCompetition:
    """Расчет рейтинга в соревновании"""
    def __init__(self, rating, instance: CompetitionModel):
        self.rating = rating
        self.instance = instance
        self.matches: list[RatingMatch] = [RatingMatch(self, match) for match in self.instance.matches]

    @property
    def service(self):
        return self.rating.service

    def __str__(self):
        return self.instance.__str__()

    def __repr__(self):
        return self.__str__()
