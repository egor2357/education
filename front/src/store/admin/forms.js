import post from "@/middleware/post";
import put from "@/middleware/put";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  forms: [],
  fetched: false,
});

const getters = {
  getForms(state) {
    return state.forms;
  },
  getFetched(state) {
    return state.fetched;
  },
};

const actions = {
  async fetchForms({ commit }) {
    try {
      let res = await this.$axios.get("/api/forms/");
      if (res.status === 200) {
        commit("setForms", {data: res.data, success: true});
      }
    } catch (e) {
      commit("setForms", {data: [], success: false});
    }
  },
  async addForm(context, payload) {
    return post(this.$axios, "/api/forms/", payload);
  },
  async editForm(context, payload) {
    return put(this.$axios, `/api/forms/${payload.id}/`, payload);
  },
  async deleteForm(context, id) {
    return deleteAxios(this.$axios, `/api/forms/${id}/`, {});
  },
  async addMethod(context, payload) {
    return post(this.$axios, "/api/methods/", payload);
  },
  async editMethod(context, payload) {
    return put(this.$axios, `/api/methods/${payload.id}/`, payload);
  },
  async deleteMethod(context, id) {
    return deleteAxios(this.$axios, `/api/methods/${id}/`, {});
  },
};

const mutations = {
  setForms(state, payload) {
    state.forms = payload.data;
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
