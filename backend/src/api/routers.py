from .players import router as router_players
from .leagues import router as router_leagues

all_routers = [
    router_players,
    router_leagues
]
