import json
import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Any
from collections import defaultdict
from src.core.service import BaseService

from src.models import CompetitionType, CompetitionModel, RatingType, PlayerModel
from src.orx.player.schemas import UpdatePlayer
from src.orx.team.schemas import CreateTeam
from src.orx.match.schemas import CreateMatch, CreateSet
from src.orx.rating.schemas import CreateRating

from .schemas import DYPScheme, CreateDYP, Team, Match


class DYP:
    def __init__(self, dyp: DYPScheme):
        self.scheme = dyp
        self.data: dict = {}
        self.competition: Optional[CompetitionModel] = None
        self.__match_counter = 0

    @property
    def match_order(self) -> int:
        self.__match_counter += 1
        return self.__match_counter

    def add(self, id: Any, obj):
        self.data[id] = obj

    def get(self, id: Any):
        return self.data.get(id)


class KickerToolDYPService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = self.uow.competitions

    async def load_by_live_link(self, link: str):
        page = requests.get(link, verify=False)
        content = page.text
        soup = BeautifulSoup(content, "lxml")
        allfd = soup.find_all('a', class_="svelte-8ynhhq", href=True)
        for h in allfd:
            __id = h["href"].split('/')[3]
            json_url = f'https://live.kickertool.de/api/table_soccer/tournaments/{__id}.json'
            print('***************', json_url)
            json_data = requests.get(json_url, verify=False)
            #json_data = json.loads(json_data_text.text)
            competition = await self.get(**{'external_id': __id})
            if competition is not None:
                continue
            await self.load_from_json(1, json_data.text)
        return True

    async def load_from_json(self, tournament_id: int, json_data) -> CompetitionModel:
        """Загрузка дипа из JSON kickertools"""
        dyp = DYP(DYPScheme(**json.loads(json_data)))
        competition = await self.update_or_create(CreateDYP(
            name=dyp.scheme.name,
            description='Загрузка из Kickertools',
            date=dyp.scheme.created_at.date(),
            type=CompetitionType.DYP,
            json_data=json_data,
            tournament_id=tournament_id,
            external_id=dyp.scheme.id
        ), **{'external_id': dyp.scheme.id})

        dyp.competition = competition
        await self.__sync_players(dyp)
        await self.__sync_qualifying(dyp)
        await self.__sync_elimination(dyp)
        await self.uow.commit()
        return competition

    async def __sync_players(self, dyp: DYP):
        """Синхронизация игроков"""

        def __participants():
            if dyp.scheme.mode == 'elimination':
                for e in dyp.scheme.eliminations:
                    for p in e.standings:
                        yield p
            else:
                for q in dyp.scheme.qualifying:
                    for p in q.participants:
                        yield p

        for p in __participants():
            try:
                last_name, first_name = filter(None, p.name.strip().split(' '))
            except:
                print(p.name)
                continue
            last_name.strip()
            first_name.strip()
            first_name.replace('ё', 'е')
            last_name.replace('ё', 'е')

            p_dict = {'first_name': first_name, 'last_name': last_name}
            # Игрок
            player = await self.uow.players.update_or_create(UpdatePlayer(**p_dict), **p_dict)
            dyp.add(p.id, player)
            # Записи о рейтингах
            rating_filter = {
                'type': RatingType.PLAYER,
                'player_id': player.id
            }
            rating = await self.uow.ratings.update_or_create(
                CreateRating(
                    league_id=None,
                    tournament_id=None,
                    **rating_filter
                ),
                **rating_filter
            )
            dyp.add((player.id, RatingType.PLAYER), rating)
            rating_league_filter = {
                'type': RatingType.LEAGUE,
                'player_id': player.id,
                'league_id': dyp.competition.tournament.league_id
            }
            rating_league = await self.uow.ratings.update_or_create(
                CreateRating(tournament_id=None, **rating_league_filter),
                **rating_league_filter
            )
            dyp.add((player.id, RatingType.LEAGUE), rating_league)
            rating_tournament_filter = {
                'type': RatingType.TOURNAMENT,
                'player_id': player.id,
                'league_id': dyp.competition.tournament.league_id,
                'tournament_id': dyp.competition.tournament_id
            }
            rating_tournament = await self.uow.ratings.update_or_create(
                CreateRating(**rating_tournament_filter),
                **rating_tournament_filter
            )
            dyp.add((player.id, RatingType.TOURNAMENT), rating_tournament)

    async def __sync_qualifying(self, dyp: DYP):
        """Синхронизация квалификации"""
        for q in dyp.scheme.qualifying:
            for r in q.rounds:
                await self.__sync_matches(dyp, r.matches)

    async def __sync_elimination(self, dyp: DYP):
        """Синхронизация плей офф"""
        for e in dyp.scheme.eliminations:
            # Winners
            for level in e.levels:
                await self.__sync_matches(dyp, level.matches)
            # Loosers
            for level in reversed(e.left_levels):
                await self.__sync_matches(dyp, level.matches)
            # Third
            await self.__sync_matches(dyp, e.third.matches)

    async def __sync_matches(self, dyp: DYP, matches: List[Match]):
        """Синхронизация списка матчей"""
        for match_scheme in matches:
            print(match_scheme)
            if match_scheme.deactivated:
                continue
            team1, team2 = await self.__sync_teams(dyp, [match_scheme.team1, match_scheme.team2])

            if team1 is None or team2 is None:
                continue
            if match_scheme.time_start is None and match_scheme.time_end is None:
                continue

            match = await self.uow.matches.update_or_create(
                CreateMatch(
                    external_id=match_scheme.id,
                    order=dyp.match_order,
                    competition_id=dyp.competition.id,
                    first_team_id=team1.id,
                    second_team_id=team2.id,
                    is_qualification=not match_scheme.is_elimination,
                    time_start=(match_scheme.time_start or match_scheme.time_end).replace(tzinfo=None)
                ),
                **{'external_id': match_scheme.id}
            )
            dyp.add(match_scheme.id, match)
            await self.__sync_sets(dyp, match_scheme, match.id)

    async def __sync_teams(self, dyp: DYP, teams: List[Team]):
        """Синхронизация комманд одного матча"""
        result = []
        for team_scheme in teams:
            if team_scheme is None:
                result.append(None)
                continue
            team = dyp.get(f'Match_Team-{team_scheme.id}')

            if team is None:
                external_second_player_id = None
                if team_scheme.players:
                    external_first_player_id = team_scheme.players[0].id
                    if len(team_scheme.players) > 1:
                        external_second_player_id = team_scheme.players[1].id
                else:
                    external_first_player_id = team_scheme.id

                first_player = dyp.get(external_first_player_id)
                second_player = dyp.get(external_second_player_id)
                team = await self.uow.teams.update_or_create(
                    CreateTeam(
                        competition_order=None,
                        external_id=f'Match_Team-{team_scheme.id}',
                        competition_id=dyp.competition.id,
                        first_player_id=first_player.id,
                        second_player_id=second_player.id if second_player else None
                    ),
                    **{'external_id': f'Match_Team-{team_scheme.id}'}
                )
                dyp.add(f'Match_Team-{team.external_id}', team)
            result.append(team)
        return result

    async def __sync_sets(self, dyp: DYP, match_scheme: Match, match_id: int):
        """Синхронизация сетов"""
        for discipline in match_scheme.disciplines:
            for order, s in enumerate(discipline.sets):
                first_team_score, second_team_score = s.scores
                set_model = await self.uow.sets.update_or_create(
                    CreateSet(
                        external_id=s.id,
                        order=order,
                        match_id=match_id,
                        first_team_score=first_team_score,
                        second_team_score=second_team_score
                    ),
                    **{'external_id': s.id}
                )
                dyp.add(s.id, set_model)

    async def update_competitition_standins(self):
        competitions = await self.uow.competitions.all(order="date")

        playears_cumulative = defaultdict(int)

        for competition in competitions:
            dyp = DYP(DYPScheme(**competition.json_data))
            for qualifying in dyp.scheme.qualifying:
                for standing in qualifying.standings:
                    last_name, first_name, *_ = filter(None, standing.name.strip().split(' '))
                    last_name.strip()
                    first_name.strip()
                    first_name.replace('ё', 'е')
                    last_name.replace('ё', 'е')
                    p_dict = {'first_name': first_name, 'last_name': last_name}
                    player = await self.uow.players.update_or_create(UpdatePlayer(**p_dict), **p_dict)
                    rating_history = await self.uow.rating_history.get_single(**{
                        'type': 'PLAYER',
                        'level': 'COMPETITION',
                        'competition_id': competition.id,
                        'player_id': player.id
                    })
                    if not rating_history:
                        continue
                    prev = await self.uow.rating_history.get_single(**{
                        'id': rating_history.prev_history_id
                    })
                    rating_history.cumulative_diff = 0
                    rating_history.cumulative = 0
                    if prev:
                        rating_history.cumulative = prev.cumulative or 0
                        playears_cumulative[player.id] = rating_history.cumulative

            for elimination in dyp.scheme.eliminations:
                for standing in elimination.standings:
                    last_name, first_name = filter(None, standing.name.strip().split(' '))
                    last_name.strip()
                    first_name.strip()
                    first_name.replace('ё', 'е')
                    last_name.replace('ё', 'е')
                    p_dict = {'first_name': first_name, 'last_name': last_name}
                    # Игрок
                    player = await self.uow.players.update_or_create(UpdatePlayer(**p_dict), **p_dict)
                    rating_history = await self.uow.rating_history.get_single(**{
                        'type': 'PLAYER',
                        'level': 'COMPETITION',
                        'competition_id': competition.id,
                        'player_id': player.id
                    })
                    if not rating_history:
                        continue
                    if not standing.stats:
                        prev = await self.uow.rating_history.get_single(**{
                            'id': rating_history.prev_history_id
                        })
                        if prev:
                            rating_history.cumulative = prev.cumulative
                            if rating_history.cumulative:
                                playears_cumulative[player.id] = rating_history.cumulative

                        continue

                    rating_history.place = standing.stats.place
                    diff = ((100 - (standing.stats.place - 1) * 10) if standing.stats.place < 11 else 5) or 0
                    rating_history.cumulative_diff = diff

                    if rating_history.prev_history_id is None:
                        rating_history.cumulative = rating_history.cumulative_diff
                        if rating_history.cumulative:
                            playears_cumulative[player.id] = rating_history.cumulative
                    else:
                        prev = await self.uow.rating_history.get_single(**{
                            'id': rating_history.prev_history_id
                        })
                        rating_history.cumulative = (prev.cumulative or 0) + rating_history.cumulative_diff
                        if rating_history.cumulative:
                            playears_cumulative[player.id] = rating_history.cumulative

        for player_id, cumulative in playears_cumulative.items():
            print('****************', player_id, cumulative)
            rating = await self.uow.ratings.get_single(**{
                'type': 'PLAYER',
                'player_id': player_id
            })
            if rating:
                rating.cumulative = cumulative

        await self.uow.commit()
        return True
