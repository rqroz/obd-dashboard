import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'
import Dashboard from '@/views/Dashboard.vue'
import DriverProfile from '@/views/DriverProfile.vue'
import LineChart from '@/views/LineChart.vue'


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
    path: '/driver-profile',
    name: 'DriverProfile',
    component: DriverProfile,
    meta: { requiresAuth: true },
  },
  {
    path: '/line-chart',
    name: 'LineChart',
    component: LineChart,
    meta: { requiresAuth: true },
  },
]

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes
});

export default router
