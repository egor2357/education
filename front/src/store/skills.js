import post from "@/middleware/post";
import put from "@/middleware/put";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({});

const getters = {};

const actions = {
  async addArea(context, payload) {
    return post(this.$axios, "/api/area/", payload);
  },
  async editArea(context, payload) {
    return put(this.$axios, `/api/area/${payload.id}`, payload);
  },
  async deleteArea(context, payload) {
    return deleteAxios(this.$axios, `/api/area/${payload.id}`, payload);
  },
  async addDirection(context, payload) {
    return post(this.$axios, "/api/direction/", payload);
  },
  async editDirection(context, payload) {
    return put(this.$axios, `/api/direction/${payload.id}`, payload);
  },
  async deleteDirection(context, payload) {
    return deleteAxios(this.$axios, `/api/direction/${payload.id}`, payload);
  },
  async addSkill(context, payload) {
    return post(this.$axios, "/api/skill/", payload);
  },
  async editSkill(context, payload) {
    return put(this.$axios, `/api/skill/${payload.id}`, payload);
  },
  async deleteSkill(context, payload) {
    return deleteAxios(this.$axios, `/api/skill/${payload.id}`, payload);
  },
};

const mutations = {};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
