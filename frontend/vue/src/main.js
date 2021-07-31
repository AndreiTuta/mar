import Vue from 'vue'
import './js/jquery-import'
import App from "./App";

Vue.config.productionTip = false;

new Vue({
  components: { App },
  render: h => h(App)
}).$mount("#app");
