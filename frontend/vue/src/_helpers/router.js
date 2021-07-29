import Vue from 'vue';
import Router from 'vue-router';

import Schedule from '../components/Schedule'
import LoginPage from '../login/LoginPage'

Vue.use(Router);

export const router = new Router({
    mode: 'history',
    routes: [
        { path: '/calendar/:id', component: Schedule },
        { path: '/login', component: LoginPage },

        // otherwise redirect to home
        { path: '*', redirect: '/login' }
    ]
});

router.beforeEach((to, from, next) => {
    // redirect to login page if not logged in and trying to access a restricted page
    const publicPages = ['/login'];
    const authRequired = !publicPages.includes(to.path);
    const loggedIn = localStorage.getItem('user');

    if (authRequired && !loggedIn) {
        return next({
            path: '/login',
            query: { returnUrl: to.path }
        });
    }

    next();
})