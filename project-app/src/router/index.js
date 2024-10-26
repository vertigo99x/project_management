import { createRouter, createWebHistory } from 'vue-router'

import store from '../store'


import Dashboard from '../views/Dashboard.vue';
import LoginView from '../views/LoginView.vue';
import Projects from '../views/Projects.vue';

import notFoundvue from '../views/notFoundvue.vue';




const routes = [
    {
        path: '/',
        name: 'dashboard',
        component: Dashboard,
        meta: { requireLogin: true }
    },
  
    {
        path: '/projects',
        name: 'projects',
        component: Projects,
        meta: { requireLogin: true }
    },

    {
        path: '/login',
        name: 'login',
        component: LoginView,
        meta: { requireLogin: false }
    },
    {
        path: '/:notFound',
        name: 'notFound',
        component: notFoundvue,
        
           
      },
]


const router = createRouter({
    history: createWebHistory(),
    routes
})


router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requireLogin) && !store.state.refresh) {
        next({ name: 'login', query: { redirect: to.fullPath } });
    } else {
        next();
    }
})

export default router
