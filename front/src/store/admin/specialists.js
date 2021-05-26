import post from "@/middleware/post";
import put from "@/middleware/put";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  specialists: [],
});

const getters = {
  getSpecialists(state) {
    return state.specialists;
  },
};

const actions = {
  async fetchSpecialists({ commit }, params = '') {
    try {
      let res = await this.$axios.get(`/api/specialists/${params}`);
      if (res.status === 200) {
        let hasAdditional = false;
        for (let spec of res.data) {
          hasAdditional = false;
          for (let activity of spec.activities) {
            if (activity.is_main === false) {
              hasAdditional = true;
              break;
            }
          }
          spec.hasAdditionalActivity = hasAdditional;
        }
        commit("setSpecialists", res.data);
      }
    } catch (e) {
      commit("setSpecialists", []);
    }
  },
  async addSpecialist(context, payload) {
    return post(this.$axios, "/api/specialists/", payload);
  },
  async editSpecialist(context, payload) {
    return put(this.$axios, `/api/specialists/${payload.id}/`, payload);
  },
  async deleteSpecialist(context, id) {
    return deleteAxios(this.$axios, `/api/specialists/${id}/`, {});
  },
  async addSpecialistActivity(context, payload) {
    return post(this.$axios, "/api/specialties/", payload);
  },
  async editSpecialistActivity(context, payload) {
    return put(this.$axios, `/api/specialties/${payload.id}/`, payload);
  },
  async deleteSpecialistActivity(context, id) {
    return deleteAxios(this.$axios, `/api/specialties/${id}/`, {});
  },
  async addSpecialistSkill(context, payload) {
    return post(this.$axios, "/api/competence/", payload);
  },
  async editSpecialistSkill(context, payload) {
    return put(this.$axios, `/api/competence/${payload.id}/`, payload);
  },
  async deleteSpecialistSkill(context, id) {
    return deleteAxios(this.$axios, `/api/competence/${id}/`, {});
  },
};

const mutations = {
  setSpecialists(state, payload) {
    state.specialists = payload;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
