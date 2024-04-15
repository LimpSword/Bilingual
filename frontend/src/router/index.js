import {createRouter, createWebHistory} from 'vue-router'
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
            path: '/login',
            name: 'login',
            component: () => import('../views/LoginView.vue')
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('../views/RegisterView.vue')
        },
        {
            path: "/signout",
            name: "signout",
            component: () => import('../views/SignoutView.vue')
        },
        {
            path: '/leaderboard',
            name: 'leaderboard',
            component: () => import('../views/LeaderboardView.vue')
        },
        {
            path: '/play',
            name: 'play',
            component: () => import('../views/AnswerView.vue')
        },
        {
            path: '/solo',
            name: 'solo',
            component: () => import('../views/SoloView.vue')
        },
        {
            path: '/new-category',
            name: 'newCategory',
            component: () => import('../views/newCategory.vue')
        },
        {
            path: '/:pathMatch(.*)*',
            name: 'not-found',
            component: () => import('../views/NotFoundView.vue')
        }
    ]
})

export default router
