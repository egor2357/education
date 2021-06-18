import post from "@/middleware/post";
import put from "@/middleware/put";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  jobs: [],
  jobsStat: {},
  fetched: false,
});

const getters = {
  getJobs(state) {
    return state.jobs;
  },
  getJobsStat(state) {
    return state.jobsStat;
  },
  getFetched(state) {
    return state.fetched;
  },
};

const actions = {
  async fetchJobs({ commit }) {
    try {
      let res = await this.$axios.get("/api/schedule/");
      if (res.status === 200) {
        commit("setJobs", {data: res.data, success: true});
        let stat = {};
        stat["sum"] = {count: 0, name: 'Всего', max: 0};
        for (let job of res.data) {
          if (stat[job.activity.id]) {
            stat[job.activity.id].count += 1;
            stat["sum"].count += 1;
          } else {
            stat[job.activity.id] = {
              name: job.activity.name,
              count: 1,
              color: job.activity.color
            };
            stat["sum"].count += 1;
          }
          if (stat["sum"].max < stat[job.activity.id].count) stat["sum"].max = stat[job.activity.id].count
        }
        commit("setJobsStat", stat)
      }
    } catch (e) {
      commit("setJobs", {data: [], success: false});
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
  clear(state){
    state.jobs = [];
    state.jobsStat = {};
    state.fetched = false;
  },
  setJobs(state, payload) {
    state.jobs = payload.data;
    state.fetched = payload.success;
  },
  setJobsStat(state, payload) {
    state.jobsStat = payload;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
