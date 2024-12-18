export default (axios) => {
  // Базовый URL модуля
  const base_url = '/players';

  return {
    async list() {
      return axios.get(`${base_url}`);
    },
    async get_competitions(page, rowsPerPage, player_id, searchString) {
      const offset = (page - 1) * rowsPerPage;
      return axios.get(`${base_url}/competitions`, {params: {
          player_id: player_id,
          limit: rowsPerPage,
          offset: offset,
          search_string: searchString
      }});
    },
    async get_player_info(player_id) {
      return axios.get(`${base_url}/${player_id}`);
    },
    async get_player_competition(player_id, competition_id){
      return axios.get(`${base_url}/player/${player_id}/competition/${competition_id}`);
    },
    async get_competition_info(competition_id){
      return axios.get(`/competition/${competition_id}`);
    },
    async get_partners(player_id){
      return axios.get(`${base_url}/partners/${player_id}`)
    },
    async get_opponents(player_id){
      return axios.get(`${base_url}/opponents/${player_id}`)
    }
  };
};
