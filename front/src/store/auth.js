const state = () => ({
  isAuth: null,
  userInfo: {
    name: null,
    staff: false,
    id: null,
    specialistId: null,
    activitiesId: [],
    skillsId: [],
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
          name: res.data.specialist ? res.data.specialist.__str__ : res.data.username,
          staff: res.data.is_staff,
          id: res.data.id,
          specialistId: res.data.specialist === null
            ? null
            : res.data.specialist.id,
          activitiesId: res.data.specialist.activities_id,
          skillsId: res.data.specialist.skills_id,
        });
      }
      return res;
    } catch (e) {
      commit("setIsAuth", false);
      commit("setUserInfo", {
        name: null,
        staff: false,
        id: null,
        specialistId: null,
        activitiesId: [],
        skillsId: [],
      });
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
        commit("setUserInfo", {
          name: null,
          staff: false,
          id: null,
          specialistId: null,
          activitiesId: [],
          skillsId: [],
        });
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
          name: res.data.specialist ? res.data.specialist.__str__ : res.data.username,
          staff: res.data.is_staff,
          id: res.data.id,
          specialistId: res.data.specialist === null
            ? null
            : res.data.specialist.id,
          activitiesId: res.data.specialist.activities_id,
          skillsId: res.data.specialist.skills_id,
        });
      }
      return res;
    } catch (e) {
      commit("setIsAuth", false);
      commit("setUserInfo", {
        name: null,
        staff: false,
        id: null,
        specialistId: null,
        activitiesId: [],
        skillsId: [],
      });
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
