import post from "@/middleware/post";
import put from "@/middleware/put";
import patch from "@/middleware/patch";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  specialists: [],
  fetched: false,
});

const getters = {
  getSpecialists(state) {
    return state.specialists;
  },
  getFetched(state) {
    return state.fetched;
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
        commit("setSpecialists", {data: res.data, success: true});
      }
    } catch (e) {
      commit("setSpecialists", {data: [], success: false});
    }
  },
  async fetchSpecialistsWithoutCommit(context, params = '') {
    try {
      let res = await this.$axios.get(`/api/specialists/${params}`);
      if (res.status === 200) {
        return {status: 200, data: res.data}
      }
    } catch (e) {
      return e
    }
  },
  async addSpecialist(context, payload) {
    return post(this.$axios, "/api/specialists/", payload);
  },
  async editSpecialist(context, payload) {
    return patch(this.$axios, `/api/specialists/${payload.id}/`, payload);
  },
  async deleteSpecialist(context, id) {
    return deleteAxios(this.$axios, `/api/specialists/${id}/`, {});
  },

  async addSpecialistActivity({ commit }, payload) {
    let res = await post(this.$axios, "/api/specialties/", payload);
    let specialistRequest = await this.$axios.get(`/api/specialists/${payload.specialist_id}/`);
    if (specialistRequest.status === 200)
      commit("updateSpecialist", specialistRequest.data);
    return res;
  },
  async editSpecialistActivity({ commit }, payload) {
    let res = await patch(this.$axios, `/api/specialties/${payload.linkId}/`, {is_main: payload.isMain});
    let specialistRequest = await this.$axios.get(`/api/specialists/${payload.specialistId}/`);
    if (specialistRequest.status === 200)
      commit("updateSpecialist", specialistRequest.data);
    return res;
  },
  async deleteSpecialistActivity({ commit }, payload) {
    let res = await deleteAxios(this.$axios, `/api/specialties/${payload.linkId}/`);
    let specialistRequest = await this.$axios.get(`/api/specialists/${payload.specialistId}/`);
    if (specialistRequest.status === 200)
      commit("updateSpecialist", specialistRequest.data);
    return res;
  },

  async addSpecialistSkill({ commit }, payload) {
    let res = await post(this.$axios, "/api/competence/", payload);
    let specialistRequest = await this.$axios.get(`/api/specialists/${payload.specialist_id}/`);
    if (specialistRequest.status === 200)
      commit("updateSpecialist", specialistRequest.data);
    return res;
  },
  async editSpecialistSkill({ commit }, payload) {
    let res = await patch(this.$axios, `/api/competence/${payload.linkId}/`, {coefficient: payload.coefficient});
    let specialistRequest = await this.$axios.get(`/api/specialists/${payload.specialistId}/`);
    if (specialistRequest.status === 200)
      commit("updateSpecialist", specialistRequest.data);
    return res;
  },
  async deleteSpecialistSkill({ commit }, payload) {
    let res = await deleteAxios(this.$axios, `/api/competence/${payload.linkId}/`);
    let specialistRequest = await this.$axios.get(`/api/specialists/${payload.specialistId}/`);
    if (specialistRequest.status === 200)
      commit("updateSpecialist", specialistRequest.data);
    return res;
  },
};

const mutations = {
  clear(state){
    state.specialists = [];
    state.fetched = false;
  },
  setSpecialists(state, payload) {
    state.specialists = payload.data;
    state.fetched = payload.success;
  },
  updateSpecialist(state, payload)
  {
    let specialist = state.specialists.find(specialist => specialist.id == payload.id);
    if (specialist){
      specialist.skills = payload.skills;
      specialist.activities = payload.activities;
      specialist.hasAdditionalActivity = !!specialist.activities.filter(activity => !activity.is_main).length;
    }
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
