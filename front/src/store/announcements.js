import post from "@/middleware/post";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  announcements: {},
  fetched: false,
  queryParams: "",
});

const getters = {
  getAnnouncements(state) {
    return state.announcements;
  },
  getQueryParams(state) {
    return state.queryParams;
  },
};

const actions = {
  async fetchAnnouncements({ state, commit }) {
    try {
      let res = await this.$axios.get(`/api/announcement/${state.queryParams}`);
      if (res.status === 200) {
        commit("setAnnouncements", { data: res.data, success: true });
        return res;
      }
    } catch (e) {
      commit("setAnnouncements", { data: {}, success: false });
      return e;
    }
  },
  async addAnnouncement(context, payload) {
    return post(this.$axios, "/api/announcement/", payload);
  },
  async deleteAnnouncement(context, id) {
    return deleteAxios(this.$axios, `/api/announcement/${id}/`, {});
  },
};

const mutations = {
  setAnnouncements(state, payload) {
    state.announcements = payload.data;
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
