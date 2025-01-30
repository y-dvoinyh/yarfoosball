export default (axios) => {
  // Базовый URL модуля
  const base_url = '/rating';

  return {
    async get_list(page, rowsPerPage, searchString, sortBy, descending) {
      const offset = (page - 1) * rowsPerPage;
      return axios.get(`${base_url}`, {params: {
          limit: rowsPerPage,
          offset: offset,
          search_string: searchString,
          sort_by: sortBy,
          descending: descending
      }});
    }
  };
};
