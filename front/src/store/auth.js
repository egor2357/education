const state = () => ({
  isAuth: true,
  userInfo: {
    name: 'Иванов И.И.',
    staff: true,
  },
});

const getters = {
  getIsAuth(state) {
    return state.isAuth;
  },
  getUserInfo(state) {
    return state.userInfo;
  },
};

const actions = {
  async login({ commit }) {
    commit("setIsAuth", true);
    commit("setUserInfo", {
      name: 'Иванов И.И.',
      staff: true,
    });
  },
  async logout({ commit }) {
    commit("setIsAuth", false);
    commit("setUserInfo", { name: null, staff: false, unit_id: null });
  },
};

const mutations = {
  setIsAuth(state, payload) {
    state.isAuth = payload;
  },
  setUserInfo(state, payload) {
    state.userInfo = payload;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
