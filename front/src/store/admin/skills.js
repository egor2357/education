import post from "@/middleware/post";
import put from "@/middleware/put";
import patch from "@/middleware/patch";
import deleteAxios from "@/middleware/deleteAxios";
import { filterByExercises } from "@/utils/skillStructureFilters";

const state = () => ({
  areas: [],
  fetched: false,
  areasAll: [],
  fetchedAll: false,
  developedSkills: [],
  developedPeriod: null,
  developedStatistics: null,
  skillDevelopmentTreeState: null,
  developedSkillsCacheTimer: null,
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
  getDevelopedSkills(state){
    return state.developedSkills;
  },
  getDevelopedPeriod(state){
    return state.developedPeriod;
  },
  getDevelopedStatistics(state){
    return state.developedStatistics;
  },
  exerciseOptions(state, getters, rootState) {
    if (rootState.auth.isAuth === null) {
      return [];
    }

    const allowedStructure = filterByExercises(
      state.areas, rootState.auth.userInfo.exercisesId
    );
    
    const options = [];
    for (let area of allowedStructure) {
      const areaNode = {
        id: 'area' + area.id,
        label: `${area.number}. ${area.name}`,
        children: []
      };
      for (let direction of area.children) {
        const directionNode = {
          id: 'direction' + direction.id,
          label: `${area.number}.${direction.number}. ${direction.name}`,
          children: [],
        }
        for (let skill of direction.children) {
          const skillNode = {
            id: 'skill' + skill.id,
            label: `${area.number}.${direction.number}.${skill.number}. ${skill.name}`,
            children: [],
          }
          for (let result of skill.children) {
            const resultNode = {
              id: 'result' + result.id,
              label: `${area.number}.${direction.number}.${skill.number}.${result.number}. ${result.name}`,
              children: [],
            }
            for (let exercise of result.children) {
              const exerciseNode = {
                id: exercise.id,
                label: `${area.number}.${direction.number}.${skill.number}.${result.number}.${exercise.number}. ${exercise.name}`,
              }

              resultNode.children.push(exerciseNode);
            }
            skillNode.children.push(resultNode);
          }
          directionNode.children.push(skillNode);
        }
        areaNode.children.push(directionNode);
      }
      options.push(areaNode);
    }
    return options;
  },
};

const actions = {
  
  async fetchAreas({commit}) {
    try {
      let res = await this.$axios.get(`/api/educational_areas/by_date/?deleted=false`);
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

  async fetchDevelopedSkills({commit}, payload){    
    if (
        !this.state.skills.developedSkillsCacheTimer // Кэш еще не устанавливался
        || this.state.skills.developedPeriod.start !== payload.start // не совпадает дата начала
        || this.state.skills.developedPeriod.end !== payload.end // не совпадает да конца
        || (new Date() - this.state.skills.developedSkillsCacheTimer > 60000)) // прошло больше минуты
    {
      try {      
        let fetches = [];
        fetches.push(this.$axios.get(`/api/educational_areas/by_interval/?start=${payload.start}&end=${payload.end}`));
        fetches.push(this.$axios.get(`/api/exercise_reports/statistics/?date_from=${payload.start}&date_to${payload.end}`));
        let responses = await Promise.all(fetches);
        if (responses[0].status === 200 && responses[1].status === 200) {
          commit("setDevelopedSkills", {structure: responses[0].data, statistics: responses[1].data, success: true, period: {start: payload.start, end: payload.end}})
        }
      }
      catch (e) {
        commit("setDevelopedSkills", {structure: [], statistics: null, success: false, period: null});
      }
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
  },
  setDevelopedSkills(state, payload){
    state.developedSkills = payload.structure;
    state.developedStatistics = payload.statistics;
    state.developedPeriod = payload.period;
    state.developedSkillsCacheTimer = new Date();
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
