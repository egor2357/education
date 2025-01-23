const state = () => ({
  notifications: {},
  socket: null,
});

const getters = {
  getNotifications(state) {
    return state.notifications;
  },
  getSocket(state) {
    return state.socket;
  },
};

const actions = {
  async fetchNotifications({ commit }) {
    try {
      let res = await this.$axios.get(`/api/notifications/calculated/`);
      if (res.status === 200) {
        commit("setNotifications", res.data);
        return res;
      }
    } catch (e) {
      commit("setNotifications", {});
      return e;
    }
  },
};

const mutations = {
  setNotifications(state, payload) {
    state.notifications = payload;
  },
  setSocket(state, payload) {
    state.socket = payload;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
