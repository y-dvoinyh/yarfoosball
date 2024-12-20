from typing import Optional
from src.core.service import BaseService


class PlayersService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = self.uow.players

    async def competitions_list(self, player_id: int, limit: int, offset: int, search_string: Optional[str]):
        if search_string is not None:
            search_string = search_string.lower()
        count = await self.repository.competitions_list_count(player_id, search_string)
        competitions = await self.repository.competitions_list(player_id, limit, offset, search_string)
        return {'count': count, 'competitions': competitions}

    async def get_player_info(self, player_id: int):
        return await self.repository.get_player_info(player_id)

    async def player_competition(self, player_id: int, competition_id: int):
        return await self.repository.player_competition(player_id, competition_id)

    async def get_partners(self, player_id):
        return await self.repository.get_partners(player_id)

    async def get_opponents(self, player_id):
        return await self.repository.get_opponents(player_id)

    async def get_player_statistic(self, player_id: int):
        return await self.repository.get_player_statictic(player_id)