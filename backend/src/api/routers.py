from .players import router as router_players
from .leagues import router as router_leagues
from .tournaments import router as router_tournaments
from .competitions import router as router_competitions

from .kickertool import router as router_kickertool
from .team_tournament import router as router_team_tournament

all_routers = [
    router_players,
    router_leagues,
    router_tournaments,
    router_competitions,

    router_kickertool,
    router_team_tournament
]
