import post from "@/middleware/post";
import put from "@/middleware/put";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  appeals: {},
  fetched: false,
  queryParams: "",
  appealInfo: {},
  messages: [],
});

const getters = {
  getAppeals(state) {
    return state.appeals;
  },
  getAppealInfo(state) {
    return state.appealInfo;
  },
  getMessages(state) {
    return state.messages;
  },
};

const actions = {
  async fetchAppeals({ state, commit }) {
    try {
      let res = await this.$axios.get(`/api/appeals/${state.queryParams}`);
      if (res.status === 200) {
        commit("setAppeals", { data: res.data, success: true });
        return res;
      }
    } catch (e) {
      commit("setAppeals", { data: {}, success: false });
      return e;
    }
  },
  async fetchAppealInfo({ state, commit, dispatch }, id) {
    try {
      let res = await this.$axios.get(`/api/appeals/${id}/`);
      if (res.status === 200) {
        commit("setAppealInfo", res.data);
        dispatch("fetchMessages", id);
        return res;
      }
    } catch (e) {
      commit("setAppeals", {});
      return e;
    }
  },
  async fetchMessages({ state, commit }, id) {
    try {
      let res = await this.$axios.get(`/api/messages/?appeal_id=${id}`);
      if (res.status === 200) {
        commit("setMessages", res.data);
        return res;
      }
    } catch (e) {
      commit("setMessages", []);
      return e;
    }
  },
  async addAppeal(context, payload) {
    return post(this.$axios, "/api/appeals/", payload);
  },
  async addMessage(context, payload) {
    return post(this.$axios, "/api/messages/", payload);
  },
  async editAppeal(context, payload) {
    return put(this.$axios, `/api/appeals/${payload.id}/`, payload);
  },
  async deleteAppeal(context, id) {
    return deleteAxios(this.$axios, `/api/appeals/${id}/`, {});
  },
  async setAppealClosed(context, id) {
    return await this.$axios.get(`/api/appeals/${id}/close/`);
  },
};

const mutations = {
  setAppeals(state, payload) {
    state.appeals = payload.data;
    state.fetched = payload.success;
  },
  setQueryParams(state, payload) {
    state.queryParams = payload;
  },
  setAppealInfo(state, payload) {
    state.appealInfo = payload;
  },
  setMessages(state, payload) {
    state.messages = payload;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
