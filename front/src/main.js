import Vue from "vue";
import App from "./App.vue";
import antdv from "@/plugins/antdv";
import router from "@/router";
import store from "@/store";
import axios from "@/plugins/axios";
import mask from "@/plugins/mask";
import 'vue-swatches/dist/vue-swatches.css';

Vue.prototype.$axios = axios;
Vue.config.productionTip = false;

new Vue({
  antdv,
  mask,
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
