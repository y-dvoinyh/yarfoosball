import json
from typing import Optional, List
from src.core.service import BaseService

from src.models.enums import CompetitionType
from src.models import CompetitionModel
from src.modules.player.schemas import CreatePlayer
from src.modules.team.schemas import CreateTeam
from src.modules.match.schemas import CreateMatch, CreateSet

from .schemas import DYPScheme, CreateDYP, Team, Match, Discipline, Set


class DYP:
    def __init__(self, dyp: DYPScheme):
        self.scheme = dyp
        self.competition: Optional[CompetitionModel] = None
        self.players_dict: Optional[dict] = {}
        self.teams_dict: Optional[dict] = {}
        self.matchs_dict: Optional[dict] = {}
        self.sets_dict: Optional[dict] = {}

    def add_player(self, id: str, player):
        self.players_dict[id] = player

    def get_player(self, id: str):
        return self.players_dict.get(id)

    def add_team(self, id: str, team):
        self.teams_dict[id] = team

    def get_team(self, id: str):
        return self.teams_dict.get(id)

    def add_match(self, id: str, match):
        self.matchs_dict[id] = match

    def get_match(self, id: str):
        return self.matchs_dict.get(id)

    def add_set(self, id: str, set_model):
        self.sets_dict[id] = set_model

    def get_set(self, id: str):
        return self.sets_dict.get(id)

    @property
    def all_teams(self) -> List[Team]:
        result = []
        team_ids = set()
        # Квалификация
        for q in self.scheme.qualifying:
            for r in q.rounds:
                for m in r.matches:
                    if m.team1.id not in team_ids:
                        team_ids.add(m.team1.id)
                        result.append(m.team1)
                    if m.team2.id not in team_ids:
                        team_ids.add(m.team2.id)
                        result.append(m.team2)
        # Плейоф - TODO
        return result

    @property
    def all_matches(self) -> List[Match]:
        result = []
        # Квалификация
        for q in self.scheme.qualifying:
            for r in q.rounds:
                for m in r.matches:
                    result.append(m)
        return result


class KickerToolDYPService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = self.uow.competitions

    async def load_from_json(self, tournament_id: int, json_data) -> CompetitionModel:
        """Загрузка дипа из JSON kickertools"""
        dyp = DYP(DYPScheme(**json.loads(json_data)))
        filters = {'external_id': dyp.scheme.id}
        competition = await self.get(**filters)
        if competition is None:
            competition = await self.create(CreateDYP(
                name=dyp.scheme.name,
                description='Загрузка из Kickertools',
                date=dyp.scheme.created_at.date(),
                type=CompetitionType.DYP,
                json_data=json_data,
                tournament_id=tournament_id
            ))
        dyp.competition = competition
        await self.__sync_players(dyp)
        await self.__sync_teams(dyp)
        await self.__sync_matches(dyp)
        await self.uow.commit()
        return competition

    async def __sync_players(self, dyp: DYP):
        """Синхронизация игроков"""
        for q in dyp.scheme.qualifying:
            for p in q.participants:
                first_name, last_name = p.name.split(' ')
                player = await self.uow.players.get_single(**{
                    'first_name': first_name,
                    'last_name': last_name
                })
                if player is None:
                    player = await self.uow.players.create(CreatePlayer(
                        first_name=first_name,
                        last_name=last_name
                    ))
                dyp.add_player(p.id, player)

    async def __sync_teams(self, dyp: DYP):
        """Синхронизация команд"""
        for team_scheme in dyp.all_teams:
            filters = {'external_id': team_scheme.id}
            team = await self.uow.teams.get_single(**filters)
            if team is None:
                external_first_player_id = team_scheme.players[0].id
                external_second_player_id = None
                if len(team_scheme.players) > 1:
                    external_second_player_id = team_scheme.players[1].id

                first_player = dyp.get_player(external_first_player_id)
                second_player = dyp.get_player(external_second_player_id)
                team = await self.uow.teams.create(CreateTeam(
                    competition_order=None,
                    external_id=team_scheme.id,
                    competition_id=dyp.competition.id,
                    first_player_id=first_player.id,
                    second_player_id=second_player.id if second_player else None
                ))
            dyp.add_team(team.external_id, team)

    async def __sync_matches(self, dyp: DYP):
        """Синхронизация матчей"""
        for order, match_scheme in enumerate(dyp.all_matches):
            filters = {'external_id': match_scheme.id}
            match = await self.uow.matches.get_single(**filters)
            if match is None:
                match = await self.uow.matches.create(CreateMatch(
                    external_id=match_scheme.id,
                    order=order,
                    competition_id=dyp.competition.id,
                    first_team_id=dyp.get_team(match_scheme.team1.id).id,
                    second_team_id=dyp.get_team(match_scheme.team2.id).id,
                    is_qualification= not match_scheme.is_elimination,
                    time_start=match_scheme.time_start
                ))
            dyp.add_match(match_scheme.id, match)
            await self.__sync_sets(dyp, match_scheme, match.id)

    async def __sync_sets(self, dyp: DYP, match_scheme: Match, match_id: int):
        for discipline in match_scheme.disciplines:
            for order, s in enumerate(discipline.sets):
                filters = {'external_id': s.id}
                set_model = await self.uow.sets.get_single(**filters)
                first_team_score, second_team_score = s.scores
                if set_model is None:
                    set_model = await self.uow.sets.create(CreateSet(
                        external_id=s.id,
                        order=order,
                        match_id=match_id,
                        first_team_score=first_team_score,
                        second_team_score=second_team_score
                    ))
                dyp.add_set(s.id, set_model)
