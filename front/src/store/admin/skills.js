import post from "@/middleware/post";
import put from "@/middleware/put";
import patch from "@/middleware/patch";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  areas: [],
  fetched: false,
  areasAll: [],
  fetchedAll: false,
  skillDevelopmentTreeState: null,
                          // {
                          //   scrollPosition: 0,
                          //   shownAreas: [],
                          //   shownDirections: [],
                          //   shownSkills: [],
                          // }
});

const getters = {
  getAreas(state) {
    return state.areas;
  },
  getAreasAll(state) {
    return state.areasAll;
  },
  getFetched(state) {
    return state.fetched;
  },
  getFetchedAll(state) {
    return state.fetchedAll;
  },
  getSkillDevelopmentTreeState(state) {
    return state.skillDevelopmentTreeState;
  },
};

const actions = {
  async fetchAreas({commit}, payload) {
    try {
      let res = await this.$axios.get(`/api/educational_areas/by_date/?deleted=${payload.deletedState}${payload.byDate ? '&by_date=' + payload.byDate : ''}`);
      if (res.status === 200) {
        commit("setAreas", {data: res.data, success: true})
      }
    }
    catch (e) {
      commit("setAreas", {data: [], success: false});
    }
  },
  async fetchAreasAll({commit}) {
    try {
      let res = await this.$axios.get("/api/educational_areas_all/");
      if (res.status === 200) {
        commit("setAreasAll", {data: res.data, success: true})
      }
    }
    catch (e) {
      commit("setAreasAll", {data: [], success: false});
    }
  },

  async addArea(context, payload) {
    return post(this.$axios, "/api/educational_areas/", payload);
  },
  async editArea(context, payload) {
    return patch(this.$axios, `/api/educational_areas/${payload.id}/`, payload);
  },
  async deleteArea(context, id) {
    return patch(this.$axios, `/api/educational_areas/${id}/set_end/`, {});
  },
  async deleteAreaForever(context, id) {
    return deleteAxios(this.$axios, `/api/educational_areas/${id}/`, {});
  },

  async addDirection(context, payload) {
    return post(this.$axios, "/api/development_directions/", payload);
  },
  async editDirection(context, payload) {
    return patch(this.$axios, `/api/development_directions/${payload.id}/`, payload);
  },
  async deleteDirection(context, id) {
    return patch(this.$axios, `/api/development_directions/${id}/set_end/`, {});
  },
  async deleteDirectionForever(context, id) {
    return deleteAxios(this.$axios, `/api/development_directions/${id}/`, {});
  },

  async addSkill(context, payload) {
    return post(this.$axios, "/api/skills/", payload);
  },
  async editSkill(context, payload) {
    return patch(this.$axios, `/api/skills/${payload.id}/`, payload);
  },
  async deleteSkill(context, id) {
    return patch(this.$axios, `/api/skills/${id}/set_end/`, {});
  },
  async deleteSkillForever(context, id) {
    return deleteAxios(this.$axios, `/api/skills/${id}/`, {});
  },

  async addResult(context, payload) {
    return post(this.$axios, "/api/results/", payload);
  },
  async editResult(context, payload) {
    return patch(this.$axios, `/api/results/${payload.id}/`, payload);
  },
  async deleteResult(context, id) {
    return patch(this.$axios, `/api/results/${id}/set_end/`, {});
  },
  async deleteResultForever(context, id) {
    return deleteAxios(this.$axios, `/api/results/${id}/`, {});
  },

  async addExercise(context, payload) {
    return post(this.$axios, "/api/exercises/", payload);
  },
  async editExercise(context, payload) {
    return patch(this.$axios, `/api/exercises/${payload.id}/`, payload);
  },
  async deleteExercise(context, id) {
    return patch(this.$axios, `/api/exercises/${id}/set_end/`, {});
  },
  async deleteExerciseForever(context, id) {
    return deleteAxios(this.$axios, `/api/exercises/${id}/`, {});
  },
  
};

const mutations = {
  clear(state){
    state.areas = [];
    state.fetched = false;
  },
  setAreas(state, payload) {
    state.areas = payload.data;
    state.fetched = payload.success;
  },
  setAreasAll(state, payload) {
    state.areasAll = payload.data;
    state.fetchedAll = payload.success;
  },
  setSkillDevelopmentTreeState(state, payload) {
    state.skillDevelopmentTreeState = payload;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
