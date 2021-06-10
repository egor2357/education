import post from "@/middleware/post";
import put from "@/middleware/put";
import patch from "@/middleware/patch";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  areas: [],
  fetched: false,
});

const getters = {
  getAreas(state) {
    return state.areas;
  },
  getFetched(state) {
    return state.fetched;
  },
};

const actions = {
  async fetchAreas({commit}) {
    try {
      let res = await this.$axios.get("/api/educational_areas/");
      if (res.status === 200) {
        commit("setAreas", res.data)
      }
    }
    catch (e) {
      commit("setAreas", [])
    }
  },
  async addArea(context, payload) {
    return post(this.$axios, "/api/educational_areas/", payload);
  },
  async editArea(context, payload) {
    return patch(this.$axios, `/api/educational_areas/${payload.id}/`, payload);
  },
  async deleteArea(context, id) {
    return deleteAxios(this.$axios, `/api/educational_areas/${id}/`, {});
  },
  async addDirection(context, payload) {
    return post(this.$axios, "/api/development_directions/", payload);
  },
  async editDirection(context, payload) {
    return patch(this.$axios, `/api/development_directions/${payload.id}/`, payload);
  },
  async deleteDirection(context, id) {
    return deleteAxios(this.$axios, `/api/development_directions/${id}/`, {});
  },
  async addSkill(context, payload) {
    return post(this.$axios, "/api/skills/", payload);
  },
  async editSkill(context, payload) {
    return patch(this.$axios, `/api/skills/${payload.id}/`, payload);
  },
  async deleteSkill(context, id) {
    return deleteAxios(this.$axios, `/api/skills/${id}/`, {});
  },
};

const mutations = {
  setAreas(state, payload) {
    state.areas = payload;
    state.fetched = true;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
