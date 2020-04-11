import { SET_LOADING_STATE } from '@/store/modules/application/mutations';
import { ENABLE_LOADING_STATE, DISABLE_LOADING_STATE } from '@/store/modules/application/actions';

export default {
  state: {
    loading: null,
  },
  getters: {
    loading: state => state.loading,
  },
  mutations: {
    [SET_LOADING_STATE](state, loading) {
      state.loading = loading;
    },
  },
  actions: {
    [ENABLE_LOADING_STATE](context) {
      context.commit(SET_LOADING_STATE, true);
    },
    [DISABLE_LOADING_STATE](context) {
      context.commit(SET_LOADING_STATE, false);
    },
  },
};
