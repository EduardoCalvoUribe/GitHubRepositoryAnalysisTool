import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/repoinfo',
      name: 'repoinfo',
      component: () => import('../views/RepositoryInfo.vue')
    },
    {
      path: '/prpage',
      name: 'pullrequests',
      component: () => import('../views/PullRequestPage.vue')
    },
    {
      path: '/commitpage',
      name: 'commits',
      component: () => import('../views/CommitPage.vue')
    },
    {
      path: '/commentpage',
      name: 'comments',
      component: () => import('../views/CommentPage.vue')
    }
  ]
})

export default router
