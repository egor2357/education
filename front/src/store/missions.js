import post from "@/middleware/post";
import put from "@/middleware/put";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  missions: {},
  fetched: false,
  queryParams: "",
});

const getters = {
  getMissions(state) {
    return state.missions;
  },
};

const actions = {
  async fetchMissions({ state, commit }) {
    try {
      let res = await this.$axios.get(`/api/missions/${state.queryParams}`);
      if (res.status === 200) {
        commit("setMissions", {data: res.data, success: true});
        return res
      }
    } catch (e) {
      commit("setMissions", {data: {}, success: false});
      return e
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
  async setExecuteMission(context, id) {
    try {
      let res = await this.$axios.get(`/api/missions/${id}/execute/`);
      if (res.status === 200) {
        return res
      } else {
        console.log(res)
      }
    } catch (e) {
      return e
    }
  },
};

const mutations = {
  setMissions(state, payload) {
    state.missions = payload.data;
    state.fetched = payload.success;
  },
  setQueryParams(state, payload) {
    state.queryParams = payload;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
