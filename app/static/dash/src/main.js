import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import requests from './plugins/requests';
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false

Vue.use(requests);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
