import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';

const BASE_URL = 'http://localhost:8000/';

axios.defaults.baseURL = BASE_URL;

axios.interceptors.response.use(
    response => response,
    error => {
        console.error("API Error:", error);
        return Promise.reject(error);
    }
);

axios.interceptors.request.use(
    config => {
        const token = store.state.access;
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    error => Promise.reject(error)
);

const app = createApp(App);

app.use(store);
app.use(router);

// Provide $http globally to all components
app.provide('$http', axios);

// Mount the app
app.mount('#app');
