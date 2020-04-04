import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

import UserModule from '@/store/modules/user';

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    user: UserModule,
  }
});
