import Vue from "vue";
import Vuex from "vuex";
import axios from "@/plugins/axios";

import auth from "@/store/auth";
import skills from "@/store/admin/skills";
import activities from "@/store/admin/activities";
import specialists from "@/store/admin/specialists";
import schedule from "@/store/admin/schedule";
import forms from "@/store/admin/forms";
import presence from "@/store/admin/presence";
import missions from "@/store/missions";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    auth,
    skills,
    activities,
    specialists,
    schedule,
    forms,
    presence,
    missions
  },
});
store.$axios = axios;

export default store;
