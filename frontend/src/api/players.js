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
    }
  };
};
