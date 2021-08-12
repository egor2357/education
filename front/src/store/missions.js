import post from "@/middleware/post";
import put from "@/middleware/put";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  missions: {},
  fetched: false,
});

const getters = {
  getMissions(state) {
    return state.missions;
  },
};

const actions = {
  async fetchMissions({ commit }) {
    try {
      let res = await this.$axios.get("/api/missions/");
      if (res.status === 200) {
        commit("setMissions", {data: res.data, success: true});
      }
    } catch (e) {
      commit("setMissions", {data: {}, success: false});
    }
  },
  async addMission(context, payload) {
    return post(this.$axios, "/api/missions/", payload);
  },
  async editMission(context, payload) {
    return put(this.$axios, `/api/missions/${payload.id}/`, payload);
  },
  async deleteMission(context, id) {
    return deleteAxios(this.$axios, `/api/missions/${id}/`, {});
  },
};

const mutations = {
  setMissions(state, payload) {
    state.missions = payload.data;
    state.fetched = payload.success;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
