import Vue from 'vue'
import Router from 'vue-router'

import Login from './components/login'
import Cyto from './components/cyto_dashboard'
Vue.use(Router)

const router = new Router({
    routes: [{
        path: '/',
        name: "login",
        component: Login
    },
    {
        path: '/cyto',
        name: "cyto",
        component: Cyto
    }]
});

export default router;