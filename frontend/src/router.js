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
      path: '/streaming',
      name: 'streaming',
      component: () => import('./views/Streaming.vue'),
      beforeEnter: authGuard
    }, 
    {
      path: '/events',
      name: 'events',
      component: () => import('./views/Events.vue'),
      beforeEnter: authGuard
    }, 
    {
      path: '/views/eventItem',
      name: 'eventItem',
      component: () => import('./views/EventItem.vue')
    }, 
    {
      path: '/views/queue',
      name: 'queue',
      component: () => import('./views/Queue.vue')
    }, 
    {
      path: '/views/seats',
      name: 'seats',
      component: () => import('./views/Seats.vue')
    }, 
    {
      path: '/views/checkout',
      name: 'checkout',
      component: () => import('./views/Checkout.vue')
    }, 
    {
      path: '/views/confirmation',
      name: 'confirmation',
      component: () => import('./views/Confirmation.vue')
    }, 
    {
      path: '/views/userProfile',
      name: 'userprofile',
      component: () => import('./views/UserProfile.vue')
    }

  ]
})

export default router
