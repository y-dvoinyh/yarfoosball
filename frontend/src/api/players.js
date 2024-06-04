export default (axios) => {
  // Базовый URL модуля
  const base_url = '/players';

  return {
    async list() {
      return axios.get(`${base_url}`);
    }
  };
};
