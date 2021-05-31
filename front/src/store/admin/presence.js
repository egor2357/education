import post from "@/middleware/post";
import put from "@/middleware/put";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  presences: [],
});

const getters = {
  getPresences(state) {
    return state.presences;
  },
};

const actions = {
  async fetchPresences({commit}, params = '') {
    try {
      let res = await this.$axios.get(`/api/presence/${params}`);
      if (res.status === 200) {
        commit("setPresences", res.data)
      }
    }
    catch (e) {
      commit("setPresences", [])
    }
  },
  async addPresence(context, payload) {
    return post(this.$axios, "/api/presence/", payload);
  },
  async editPresence(context, payload) {
    return put(this.$axios, `/api/presence/${payload.id}/`, payload);
  },
  async deletePresence(context, id) {
    return deleteAxios(this.$axios, `/api/presence/${id}/`, {});
  },
};

const mutations = {
  setPresences(state, payload) {
    state.presences = payload;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
