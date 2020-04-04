import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import requests from './plugins/requests';
import vuetify from './plugins/vuetify';
import filters from './plugins/filters';


Vue.config.productionTip = false

Vue.use(requests);
Vue.use(filters);


// Set up for Router so that it handles auth and unauth reidrects automatically
router.beforeEach((to, from, next) => {
  const isAuth = store.getters.user !== null;
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuth) {
      next({name: 'Index', query: { redirect: to.fullPath } });
      return;
  }

  if (to.matched.some(record => record.meta.requiresUnauth) && isAuth) {
    next({ name: 'Dashboard' });
    return;
  }

  next();
});


new Vue({
  router,
  store,
  vuetify,
  computed: {
    isAuthenticated() {
      return this.$store.getters.user != null;
    },
  },
  watch: {
    isAuthenticated(newValue, oldValue) {
      if (oldValue === false && newValue === true) {
        // User just authenticated
        router.push(
          this.$route.query.redirect ||
          { name: this.$route.name === 'Index' ? 'Dashboard' : this.$route.name }
        );
      } else if (newValue === false && oldValue === true) {
        // User got logged out
        this.$router.push({ name: 'Index' });
      }
    },
  },
  render: h => h(App)
}).$mount('#app')
