import post from "@/middleware/post";
import put from "@/middleware/put";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  talents: {},
  fetched: false,
  queryParams: "",
});

const getters = {
  getTalents(state) {
    return state.talents;
  },
};

const actions = {
  async fetchTalents({ state, commit }) {
    try {
      let res = await this.$axios.get(`/api/talents/${state.queryParams}`);
      if (res.status === 200) {
        commit("setTalents", {data: res.data, success: true});
        return res
      }
    } catch (e) {
      commit("setTalents", {data: {}, success: false});
      return e
    }
  },
  async addTalent(context, payload) {
    return post(this.$axios, "/api/talents/", payload);
  },
  async editTalent(context, payload) {
    return put(this.$axios, `/api/talents/${payload.id}/`, payload);
  },
  async deleteTalent(context, id) {
    return deleteAxios(this.$axios, `/api/talents/${id}/`, {});
  },
};

const mutations = {
  setTalents(state, payload) {
    state.talents = payload.data;
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
