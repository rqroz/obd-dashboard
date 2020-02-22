import Vue from 'vue';
import App from '@/App';

import '@/plugins/axios';
import '@/plugins/blockui';
import '@/plugins/chartist';
import '@/plugins/components';
import vuetify from '@/plugins/vuetify';
import router from '@/plugins/router';
import store from '@/store';


Vue.config.productionTip = false;


new Vue({
  router,
  store,
  vuetify,
  data: () => ({
    snackbar: {
      display: false,
      timeout: 5 * 1000,
      html: null,
      color: null,
      multiline: true,
    },
    blocker: {
      defaultMessage: 'Por favor, aguarde...',
      message: null,
      display: false,
    },
  }),
  computed: {
    isDisplayingSnackbar() {
      return this.snackbar.display;
    },
  },
  watch: {
    isDisplayingSnackbar(value) {
      if (!value) {
        this.snackbar.html = null;
        this.snackbar.color = null;
      }
    },
  },
  methods: {
    toast(html, color) {
      this.snackbar.html = html;
      this.snackbar.color = color;
      this.snackbar.display = true;
    },
    blockUI(message) {
      this.blocker.message = message || this.blocker.defaultMessage;
      this.blocker.display = true;
    },
    releaseUI() {
      this.blocker.message = null;
      this.blocker.display = false;
    },
  },
  render: h => h(App),
}).$mount('#app');
