const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') }
    ]
  },
  {
    path: '/player/:id',
    props: true,
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {name: 'player_page_route', path: '', props: true, component: () => import('pages/PlayerPage.vue') }
    ]
  },
  {
    path: '/players/:id/competition/::competition_id/',
    props: true,
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {name: 'competition_page_route', path: '', props: true, component: () => import('pages/CompetitionPage.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
