import post from "@/middleware/post";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  announcements: {},
  fetched: false,
});

const getters = {
  getAnnouncements(state) {
    return state.announcements;
  },
};

const actions = {
  async fetchAnnouncements({ state, commit }) {
    try {
      let res = await this.$axios.get(`/api/announcement/`);
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
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
