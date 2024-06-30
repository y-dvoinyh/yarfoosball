from .service import RatingService
from .competition import RatingCompetition


class Rating:
    """
    Основной класс для расчета рейтинга
    """
    def __init__(self, service: RatingService):
        self.service = service
        self.competitons: list[RatingCompetition] = []
        self.leagues: list = []

    async def calculate(self):
        """Запустить расчет рейтингов"""
        competitions = await self.service.competitions()
        self.competitons = [RatingCompetition(self, c) for c in competitions]

        for c in self.competitons:
            print(c)
            for m in c.matches:
                print(m)
                print(m.first_team)
                print(m.second_team)
                rating = await m.first_team.rating
                print(rating)

        await self.service.uow.commit()
