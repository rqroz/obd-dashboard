import {
  SET_USER, UNSET_USER,
} from '@/store/modules/user/mutations';

import {
  DEFINE_USER, CLEAR_USER,
} from '@/store/modules/user/actions';

export default {
  state: {
    user: null,
  },
  getters: {
    user: state => state.user,
  },
  mutations: {
    [SET_USER](state, user) {
      state.user = user;
      localStorage.user = JSON.stringify(user);
    },
    [UNSET_USER](state) {
      state.paymentMethods = [];
      localStorage.removeItem('user');
    },
  },
  actions: {
    [DEFINE_USER](context, playload) {
      context.commit(SET_USER, playload.user);
    },
    [CLEAR_USER](context) {
      context.commit(UNSET_USER);
    },
  },
};
