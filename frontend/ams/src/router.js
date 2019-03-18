import Vue from 'vue'
import Router from 'vue-router'

import Login from './components/login'
import Cyto from './components/cyto_dashboard'
import Admin from './components/admin_dashboard'
import User from './components/user_dashboard'
import Signout from './components/signout'
import Cyto2 from './components/cyto_dashboard2'

Vue.use(Router)

const router = new Router({
    routes: [{
        path: '/',
        name: "login",
        component: Login
    },
    {
        path: "/signout",
        name: "signout",
        component: Signout
    },
    {
        path: '/cyto',
        name: "Dashboard",
        component: Cyto2
    },
    {
        path: '/admin',
        name: 'Admin Dashboard',
        component: Admin
    },
    {
        path: '/userprofile',
        name: 'User Dashboard',
        component: User
    }]
});

export default router;