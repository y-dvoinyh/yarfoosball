import { boot } from 'quasar/wrappers'
import axios from 'axios'

/** Базовая конфигурация axios */
const api_config = {
  baseURL: process.env.BASE_API_URL
}
/** Создание экземпляра axios */
const api = axios.create(api_config);

/** Перехватчики токена авторизации */
const authInterceptor = config => {
  // достаём токент аутентификации пользователя, с LocalStorage, или cookies, например
  const authToken = '...';
  config.headers.Authorization = `Bearer ${authToken}`;

  return config;
};

/** добавлени логгера при каждом axios запросе */
const loggerInterceptor = config => {
  /** как-то обрабатываем логи */
  return config;
};

/** Добавляем экземпляру созданные обработчики для аутентификации и логов */
api.interceptors.request.use(authInterceptor);
api.interceptors.request.use(loggerInterceptor);

/** Добавление обработчика для результатов или ошибок при запросах */
api.interceptors.response.use(
  response => {
    /** Как-то обрабатываем успешный результат */
    return response;
  },
  error => {
    /** Как-то обрабатываем результат, завершенный ошибкой */
    return Promise.reject(error);
  }
);

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
// const api = axios.create({ baseURL: 'https://api.example.com' })

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
})

export { axios, api }
