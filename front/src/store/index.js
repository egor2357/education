import Vue from "vue";
import Vuex from "vuex";
import axios from "@/plugins/axios";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {},
});
store.$axios = axios;

export default store;
