import Vue from 'vue';
import VueRouter from 'vue-router';
import Index from '@/components/Index';
import Login from '@/components/auth/Login';


Vue.use(VueRouter);


export default new VueRouter({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '*',
      redirect: { name: 'Index' },
    }
  ],
});
