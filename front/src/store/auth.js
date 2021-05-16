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
    try {
      let res = await this.$axios.post("/api/login/", payload);
      if (res.status === 200) {
        commit("setIsAuth", true);
        commit("setUserInfo", {
          name: res.data.fullname,
          staff: res.data.is_staff,
        });
      }
      return res;
    } catch (e) {
      commit("setIsAuth", false);
      commit("setUserInfo", { name: null, staff: false, });
      if (e.response) {
        return e.response;
      } else {
        return e;
      }
    }
  },
  async logout({ commit }) {
    try {
      let res = await this.$axios.post("/api/logout/");
      if (res.status === 200) {
        commit("setIsAuth", false);
        commit("setUserInfo", { name: null, staff: false });
      }
      return res;
    } catch (e) {
      if (e.response) {
        return e.response;
      } else {
        return e;
      }
    }
  },
  async checkUser({ commit }) {
    try {
      let res = await this.$axios.get("/api/user/?current=true");
      if (res.status === 200) {
        commit("setIsAuth", true);
        commit("setUserInfo", {
          name: res.data.results[0].fullname,
          staff: res.data.results[0].is_staff,
        });
      }
      return res;
    } catch (e) {
      commit("setIsAuth", false);
      commit("setUserInfo", { name: null, staff: false });
      if (e.response) {
        return e.response;
      } else {
        return e;
      }
    }
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
