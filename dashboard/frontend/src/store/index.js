// Lib imports
import Vue from 'vue';
import Vuex from 'vuex';

// Store functionality
import actions from './actions';
import getters from './getters';
import modules from './modules';
import mutations from './mutations';
import state from './state';


Vue.use(Vuex);


export default new Vuex.Store({
  strict: process.env.NODE_ENV === 'development',
  actions,
  getters,
  modules,
  mutations,
  state,
});
