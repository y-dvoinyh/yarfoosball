import json
from typing import Optional, List
from src.core.service import BaseService

from src.models.enums import CompetitionType
from src.models import CompetitionModel
from src.orx.player.schemas import UpdatePlayer
from src.orx.team.schemas import CreateTeam
from src.orx.match.schemas import CreateMatch, CreateSet

from .schemas import DYPScheme, CreateDYP, Team, Match


class DYP:
    def __init__(self, dyp: DYPScheme):
        self.scheme = dyp
        self.data: dict = {}
        self.competition: Optional[CompetitionModel] = None

        self.sets_dict: Optional[dict] = {}

    def add(self, id: str, obj):
        self.data[id] = obj

    def get(self, id: str):
        return self.data.get(id)

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
        await self.__sync_teams(dyp)
        await self.__sync_matches(dyp)
        await self.uow.commit()
        return competition

    async def __sync_players(self, dyp: DYP):
        """Синхронизация игроков"""
        for q in dyp.scheme.qualifying:
            for p in q.participants:
                first_name, last_name = p.name.split(' ')
                p_dict = {'first_name': first_name, 'last_name': last_name}
                player = await self.uow.players.update_or_create(UpdatePlayer(**p_dict), **p_dict)
                dyp.add(p.id, player)

    async def __sync_teams(self, dyp: DYP):
        """Синхронизация команд"""
        for team_scheme in dyp.all_teams:
            external_first_player_id = team_scheme.players[0].id
            external_second_player_id = None
            if len(team_scheme.players) > 1:
                external_second_player_id = team_scheme.players[1].id

            first_player = dyp.get(external_first_player_id)
            second_player = dyp.get(external_second_player_id)
            team = await self.uow.teams.update_or_create(
                CreateTeam(
                    competition_order=None,
                    external_id=team_scheme.id,
                    competition_id=dyp.competition.id,
                    first_player_id=first_player.id,
                    second_player_id=second_player.id if second_player else None
                ),
                **{'external_id': team_scheme.id}
            )
            dyp.add(team.external_id, team)

    async def __sync_matches(self, dyp: DYP):
        """Синхронизация матчей"""
        for order, match_scheme in enumerate(dyp.all_matches):
            match = await self.uow.matches.update_or_create(
                CreateMatch(
                    external_id=match_scheme.id,
                    order=order,
                    competition_id=dyp.competition.id,
                    first_team_id=dyp.get(match_scheme.team1.id).id,
                    second_team_id=dyp.get(match_scheme.team2.id).id,
                    is_qualification=not match_scheme.is_elimination,
                    time_start=match_scheme.time_start.replace(tzinfo=None)
                ),
                **{'external_id': match_scheme.id}
            )
            dyp.add(match_scheme.id, match)
            await self.__sync_sets(dyp, match_scheme, match.id)

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
