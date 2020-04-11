import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

import AppModule from '@/store/modules/application';
import UserModule from '@/store/modules/user';

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    app: AppModule,
    user: UserModule,
  }
});
