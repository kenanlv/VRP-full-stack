import Vue from 'vue'
import VueRouter from 'vue-router'
import vuetify from '@/plugins/vuetify'
import App from './App.vue'
import LandingPage from "./components/LandingPage"
import EditInfo from "./components/EditInfo";
import Success from "./components/Success";
// import 'bootstrap'
// import 'bootstrap/dist/css/bootstrap.min.css'
import '@fortawesome/fontawesome-free/css/all.css'

Vue.config.productionTip = false;
Vue.use(VueRouter);

const routes = [
    {path: '/', component: LandingPage},
    {path: '/info', component: EditInfo},
    {path: '/success', component: Success}
];

const router = new VueRouter({
    routes
});

router.beforeEach((to, from, next) => {
    if (window.localStorage.getItem("AccessToken")) {
        if (to.path === '/') {
            next('/info')
        } else {
            next()
        }
    } else {
        if (to.path !== '/') {
            next('/')
        } else {
            next()
        }
    }
});

new Vue({
    vuetify,
    router,
    render: h => h(App),
}).$mount('#app');
