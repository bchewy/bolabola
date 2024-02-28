import { createRouter, createWebHistory } from 'vue-router'
import { authGuard } from "@auth0/auth0-vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
			component: () => import('./views/Home.vue')

    },
    {
      path: '/about',
      name: 'about',
      component: () => import('./views/About.vue')
    }, 
    {
      path: '/events',
      name: 'events',
      component: () => import('./views/Events.vue')
    }, 

  ]
})

export default router
