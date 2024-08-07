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
      path: '/admin',
      name: 'admin',
      component: () => import('./views/Admin.vue'),
      beforeEnter: authGuard
    },


    // {
    //   path: '/views/eventItem',
    //   name: 'eventItem',
    //   component: () => import('./views/EventItem.vue')
    // }, 

    {
      path: '/views/queue/:id',
      name: 'Queue',
      component: () => import('./views/Queue.vue'),
      props: true,
      beforeEnter: authGuard
    },

    {
      path: '/views/seats/:id',
      name: 'seats',
      component: () => import('./views/Seats.vue'),
      props: true,
      beforeEnter: authGuard
    },
    {
      path: '/views/checkout/:id',
      name: 'checkout',
      component: () => import('./views/Checkout.vue'),
      props: true,
      beforeEnter: authGuard
    },
    {
      path: '/views/checkoutSuccess',
      name: 'checkoutSuccess',
      component: () => import('./views/CheckoutSuccess.vue'),
      beforeEnter: authGuard
    },
    {
      path: '/views/checkoutCancel',
      name: 'checkoutCancel',
      component: () => import('./views/CheckoutCancel.vue'),
      beforeEnter: authGuard
    },
    {
      path: '/profile',
      name: 'userprofile',
      component: () => import('./views/UserProfile.vue'),
      beforeEnter: authGuard
    },
    {
      path: '/views/refund',
      name: 'refund',
      component: () => import('./views/Refund.vue'),
      beforeEnter: authGuard
    },

    // Streaming extras
    {
      path: '/streaming/:id',
      name: 'Streaming',
      component: () => import('./views/Streaming.vue'),
      beforeEnter: authGuard,
      props: true,
    },




  ]
})

export default router
