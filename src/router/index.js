import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import FirstLevelView from '@/views/FirstLevelView.vue'
import SecondLevelView from '@/views/SecondLevelView.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: HomeView,
        },
        {
            path: '/categorias/:categoryName',
            component: FirstLevelView,
            props: true,
        },
        {
            path: '/categorias/:categoryName/:merchantName',
            name: 'merchant',
            component: SecondLevelView,
            props: true,
        },
        {path: '/categorias', component: () => import('@/views/CategoriesView.vue')},
    ]  
})

export default router