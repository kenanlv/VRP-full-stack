import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import LandingPage from "@/components/LandingPage"
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import '@fortawesome/fontawesome-free/css/all.css'

Vue.config.productionTip = false;
Vue.use(VueRouter);

const routes = [
    { path: '/', component: LandingPage}
];

const router = new VueRouter({
    routes
});

new Vue({
    router,
    render: h => h(App),
}).$mount('#app');
