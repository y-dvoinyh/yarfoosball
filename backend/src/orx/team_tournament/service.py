import json
from src.core.service import BaseService
from src.models.enums import TournamentType, CompetitionType
from src.orx.player.schemas import UpdatePlayer
from src.orx.tournament.schemas import CreateTournamentTeam
from src.orx.team.schemas import CreateTeam
from src.orx.match.schemas import CreateMatch, CreateSet

from .schemas import TeamTournament, CreateTeamTournament, CreateTeamCompetition, Competition, Match


class TTournament:
    def __init__(self, tt: TeamTournament):
        self.tournament = None
        self.scheme = tt
        self.data: dict = {}

    def add(self, id: str, obj):
        self.data[id] = obj

    def get(self, id: str):
        return self.data.get(id)


class TeamTournamentService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = self.uow.tournaments

    async def load_from_json(self, league_id: int, json_data):
        """Загрузка командного турнира"""
        tt = TTournament(TeamTournament(**json.loads(json_data)))

        tournament = await self.update_or_create(
            CreateTeamTournament(
                external_id=tt.scheme.id,
                name=tt.scheme.name,
                description='Загружено из JSON',
                type=TournamentType.TEAM,
                league_id=league_id,
                json_data=json_data
            ),
            external_id=tt.scheme.id
        )
        tt.tournament = tournament

        await self.__sync_players(tt)
        await self.__sync_tournament_teams(tt)
        await self.__sync_competitions(tt)

        await self.uow.commit()
        return tournament

    async def __sync_players(self, tt: TTournament):
        """Синхронизация игроков"""
        for player_scheme in tt.scheme.players:
            first_name, last_name = player_scheme.name.split(' ')
            player_dict = {"first_name": first_name, "last_name": last_name}
            player = await self.uow.players.update_or_create(
                UpdatePlayer(**player_dict),
                **player_dict
            )
            tt.add(player_scheme.id, player)

    async def __sync_tournament_teams(self, tt: TTournament):
        """Синхронизация команд турнира"""
        for team_scheme in tt.scheme.teams:
            team = await self.uow.tournament_teams.update_or_create(CreateTournamentTeam(
                name=team_scheme.name,
                tournament_id=tt.tournament.id,
                external_id=team_scheme.id,
                players=json.dumps([tt.get(p).id for p in team_scheme.players])
            ), **{'external_id': team_scheme.id})
            tt.add(team_scheme.id, team)

    async def __sync_competitions(self, tt: TTournament):
        """Синхронизация соревнований"""
        for c_scheme in tt.scheme.competitions:

            competition = await self.uow.competitions.update_or_create(CreateTeamCompetition(
                tournament_id=tt.tournament.id,
                name=c_scheme.name,
                description=(c_scheme.table_name or '') + '; '.join(c_scheme.video_lincs),
                date=c_scheme.start_datetime.date(),
                type=CompetitionType.TEAM,
                external_id=c_scheme.id
            ), **{'external_id': c_scheme.id})
            tt.add(c_scheme.id, competition)
            await self.__sync_teams(tt, c_scheme, competition.id)
            await self.__sync_matches(tt, c_scheme, competition.id)

    async def __sync_teams(self, tt: TTournament, competition: Competition, competition_id):
        teams = []
        for m in competition.matches:
            teams.append(m.first_team)
            teams.append(m.second_team)

        for steam in teams:
            first_player = tt.get(steam.players[0])
            second_player = None
            if len(steam.players) > 1:
                second_player = tt.get(steam.players[1])
            team = await self.uow.teams.update_or_create(
                CreateTeam(
                    competition_order=None,
                    external_id=steam.id,
                    competition_id=competition_id,
                    first_player_id=first_player.id,
                    second_player_id=second_player.id if second_player else None
                ),
                **{'external_id': steam.id}
            )
            tt.add(steam.id, team)

    async def __sync_matches(self, tt: TTournament, competition: Competition, competition_id):
        """Синхронизация сетов"""
        for order, smatch in enumerate(competition.matches):
            match = await self.uow.matches.update_or_create(CreateMatch(
                external_id=smatch.id,
                order=order,
                competition_id=competition_id,
                first_team_id=tt.get(smatch.first_team.id).id,
                second_team_id=tt.get(smatch.second_team.id).id,
                is_qualification=False,
                #time_start=smatch.time_start.replace(tzinfo=None)
            ), **{'external_id': smatch.id})
            tt.add(smatch.id, match)
            await self.__sync_sets(tt, smatch, match.id)

    async def __sync_sets(self, tt: TTournament, match_scheme: Match, match_id: int):
        for order, s in enumerate(match_scheme.sets):
            first_team_score, second_team_score = s.score
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
            tt.add(s.id, set_model)
