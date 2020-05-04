import axios from 'axios';

const requests = axios.create({
  baseURL: '/api/',
  timeout: 30 * 1000,
  headers: {
    'Content-Type': 'application/json',
  },
});


const VueRequestsPlugin = {
  install(Vue) {
    if (!Object.prototype.hasOwnProperty.call(Vue, '$requests')) {
      Object.defineProperty(Vue.prototype, '$requests', {
        get: function get() { return requests }
      });
    }
  }
};

export default VueRequestsPlugin;
