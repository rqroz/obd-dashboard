import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'
import Dashboard from '@/views/Dashboard.vue'
import Driver from '@/views/Driver.vue'
import Engine from '@/views/Engine.vue'
import Fuel from '@/views/Fuel.vue'


Vue.use(VueRouter)


const routes = [
  {
    path: '/',
    name: 'Index',
    component: Home,
    meta: { requiresUnauth: true },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true },
  },
  {
    path: '/driver',
    name: 'Driver',
    component: Driver,
    meta: { requiresAuth: true },
  },
  {
    path: '/engine',
    name: 'Engine',
    component: Engine,
    meta: { requiresAuth: true },
  },
  {
    path: '/fuel',
    name: 'Fuel',
    component: Fuel,
    meta: { requiresAuth: true },
  },
]

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes
});

export default router
