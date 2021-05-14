import Vue from "vue";
import Vuex from "vuex";
import axios from "@/plugins/axios";

import auth from "@/store/auth"

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    auth: auth
  },
});
store.$axios = axios;

export default store;
