import Vue from "vue";
import Vuex from "vuex";
import axios from "@/plugins/axios";

import auth from "@/store/auth";
import skills from "@/store/admin/skills";
import activities from "@/store/admin/activities";
import specialists from "@/store/admin/specialists";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    auth,
    skills,
    activities,
    specialists
  },
});
store.$axios = axios;

export default store;
