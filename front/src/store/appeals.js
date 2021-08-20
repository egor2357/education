import post from "@/middleware/post";
import put from "@/middleware/put";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  appeals: {},
  fetched: false,
  queryParams: "",
});

const getters = {
  getAppeals(state) {
    return state.appeals;
  },
};

const actions = {
  async fetchAppeals({ state, commit }) {
    try {
      let res = await this.$axios.get(`/api/appeals/${state.queryParams}`);
      if (res.status === 200) {
        commit("setAppeals", {data: res.data, success: true});
        return res
      }
    } catch (e) {
      commit("setAppeals", {data: {}, success: false});
      return e
    }
  },
  async addAppeal(context, payload) {
    return post(this.$axios, "/api/appeals/", payload);
  },
  async editAppeal(context, payload) {
    return put(this.$axios, `/api/appeals/${payload.id}/`, payload);
  },
  async deleteAppeal(context, id) {
    return deleteAxios(this.$axios, `/api/appeals/${id}/`, {});
  },
};

const mutations = {
  setAppeals(state, payload) {
    state.appeals = payload.data;
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
