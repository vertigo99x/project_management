import { createRouter, createWebHistory } from 'vue-router'

import store from '../store'


import Dashboard from '../views/Dashboard.vue';
import LoginView from '../views/LoginView.vue';
import  GateManagement from '../views/GateManagement.vue';
import Projects from '../views/Projects.vue';
import JobView from '../views/JobView.vue';

import Profile from '../views/Profile.vue'

import notFoundvue from '../views/notFoundvue.vue';




const routes = [
    {
        path: '/',
        name: 'dashboard',
        component: Dashboard,
        meta: { requireLogin: true }
    },
    {
        path: '/security',
        name: 'security',
        component: GateManagement,
        meta: { requireLogin: true }
    },
    {
        path: '/projects',
        name: 'projects',
        component: Projects,
        meta: { requireLogin: true }
    },
    {
        path: '/jobs',
        name: 'jobs',
        component: JobView,
        meta: { requireLogin: true }
    },
    {
        path: '/profile',
        name: 'profile',
        component: Profile,
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
    } else if (store.state.usercat === 'security_officer' && to.matched.some(record => record.meta.requireLogin)) {
        const allowedForSecurity = ['dashboard', 'security','profile']; 
        if (!allowedForSecurity.includes(to.name)) {
          next({ name: 'dashboard', query: { to: to.path } });
        } else {
          next(); // Allow access to allowed routes
        }
    
    } else if (store.state.usercat === 'maintenance_supervisor' && to.matched.some(record => record.meta.requireLogin)) {
        const allowedForSupervisor = ['dashboard', 'projects', 'jobs', 'profile']; 
        if (!allowedForSupervisor.includes(to.name)) {
          next({ name: 'dashboard', query: { to: to.path } });
        } else {
          next(); // Allow access to allowed routes
        }
    
    } else {
        next();
    }
})

export default router
