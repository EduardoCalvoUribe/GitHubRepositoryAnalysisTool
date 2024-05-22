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
      path: '/userpage',
      name: 'user',
      component: () => import('../views/UserPage.vue')
    },
    {
      path: '/repoinfo/:id',
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
