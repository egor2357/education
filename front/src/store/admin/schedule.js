import post from "@/middleware/post";
import put from "@/middleware/put";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  jobs: [],
});

const getters = {
  getJobs(state) {
    return state.jobs;
  },
};

const actions = {
  async fetchJobs({ commit }) {
    try {
      let res = await this.$axios.get("/api/schedule/");
      if (res.status === 200) {
        commit("setJobs", res.data);
      }
    } catch (e) {
      commit("setJobs", []);
    }
  },
  async addJob(context, payload) {
    return post(this.$axios, "/api/schedule/", payload);
  },
  async editJob(context, payload) {
    return put(this.$axios, `/api/schedule/${payload.id}/`, payload);
  },
  async deleteJob(context, id) {
    return deleteAxios(this.$axios, `/api/schedule/${id}/`, {});
  },
};

const mutations = {
  setJobs(state, payload) {
    state.jobs = payload;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
