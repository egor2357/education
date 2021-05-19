const state = () => ({
  isAuth: null,
  userInfo: {
    name: null,
    staff: false,
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
  async login({ commit }, payload) {
    try {
      let res = await this.$axios.post("/api/users/login/", payload);
      if (res.status === 200) {
        commit("setIsAuth", true);
        commit("setUserInfo", {
          name:
            res.data.specialist !== null && res.data.specialist.surname
              ? `${res.data.specialist.surname} ${res.data.specialist.name[0]}. ${res.data.specialist.patronymic[0]}.`
              : res.data.username,
          staff: res.data.is_staff,
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
  async logout({ commit }) {
    try {
      let res = await this.$axios.get("/api/users/logout/");
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
      let res = await this.$axios.get("/api/users/current");
      if (res.status === 200) {
        commit("setIsAuth", true);
        commit("setUserInfo", {
          name:
            res.data.specialist !== null && res.data.specialist.surname
              ? `${res.data.specialist.surname} ${res.data.specialist.name[0]}. ${res.data.specialist.patronymic[0]}.`
              : res.data.username,
          staff: res.data.is_staff,
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
