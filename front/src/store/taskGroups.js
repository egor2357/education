import post from "@/middleware/post";
import put from "@/middleware/put";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  taskGroups: {},
  fetched: false,
  queryParams: "",
});

const getters = {
  getTaskGroups(state) {
    return state.taskGroups;
  },
};

const actions = {
  async fetchTaskGroups({ state, commit }) {
    try {
      let res = await this.$axios.get(`/api/task_groups/${state.queryParams}`);
      if (res.status === 200) {
        commit("setTaskGroups", { data: res.data, success: true });
        return res;
      }
    } catch (e) {
      commit("setTaskGroups", { data: {}, success: false });
      return e;
    }
  },
  async addTaskGroup(context, payload) {
    return post(this.$axios, "/api/task_groups/", payload);
  },
  async editTaskGroup(context, payload) {
    return put(this.$axios, `/api/task_groups/${payload.id}/`, payload);
  },
  async deleteTaskGroup(context, id) {
    return deleteAxios(this.$axios, `/api/task_groups/${id}/`, {});
  },
};

const mutations = {
  setTaskGroups(state, payload) {
    state.taskGroups = payload.data;
    state.fetched = payload.success;
  },
  setQueryParams(state, payload) {
    state.queryParams = payload;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
