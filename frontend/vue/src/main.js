import Vue from 'vue'
import './js/jquery-import'
import App from './App'
import { router } from './_helpers/router'
import { configureFakeBackend } from "./_helpers/fake-backend";

configureFakeBackend();
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
