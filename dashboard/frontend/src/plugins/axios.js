import Vue from 'vue';
import axios from 'axios';

const requests = axios.create({
  baseURL: '/',
  timeout: 15 * 1000,
  headers: {
    'Content-Type': 'application/json',
  },
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
});

if (!Vue.prototype.hasOwnProperty('$requests')) {
  Object.defineProperty(Vue.prototype, '$requests', {
    get: function get() { return requests; }
  });
}
