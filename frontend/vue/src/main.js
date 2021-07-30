import Vue from 'vue'
import './js/jquery-import'
import App from './App'
import { router } from './_helpers/router'
import { configureUserPool } from "./_helpers/userService";

configureUserPool();
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
