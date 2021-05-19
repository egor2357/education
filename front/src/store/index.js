import Vue from "vue";
import Vuex from "vuex";
import axios from "@/plugins/axios";

import auth from "@/store/auth";
import skills from "@/store/skills";
import activities from "@/store/activities";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    auth,
    skills,
    activities
  },
});
store.$axios = axios;

export default store;
