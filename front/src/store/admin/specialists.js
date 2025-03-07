import post from "@/middleware/post";
import put from "@/middleware/put";
import patch from "@/middleware/patch";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  specialists: [],
  fetched: false,
  onlySpecialists: [],
  onlyAdmins: [],
});

const getters = {
  getSpecialists(state) {
    return state.specialists;
  },
  getFetched(state) {
    return state.fetched;
  },
  getOnlySpecialists(state) {
    return state.onlySpecialists;
  },
  getOnlyAdmins(state) {
    return state.onlyAdmins;
  },
};

const actions = {
  async fetchSpecialists({ commit }, params = "") {
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
        commit("setSpecialists", { data: res.data, success: true });
        commit(
          "setOnlySpecialists",
          res.data
            .filter((item) => !item.user.is_staff)
            .map((item) => {
              return item;
            })
        );
        commit(
          "setOnlyAdmins",
          res.data
            .filter((item) => item.user.is_staff)
            .map((item) => {
              return item;
            })
        );
      }
    } catch (e) {
      commit("setSpecialists", { data: [], success: false });
    }
  },
  async fetchSpecialistsWithoutCommit(context, params = "") {
    try {
      let res = await this.$axios.get(`/api/specialists/${params}`);
      if (res.status === 200) {
        return { status: 200, data: res.data };
      }
    } catch (e) {
      return e;
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
    let specialistRequest = await this.$axios.get(
      `/api/specialists/${payload.specialist_id}/`
    );
    if (specialistRequest.status === 200)
      commit("updateSpecialist", specialistRequest.data);
    return res;
  },
  async editSpecialistActivity({ commit }, payload) {
    let res = await patch(this.$axios, `/api/specialties/${payload.linkId}/`, {
      is_main: payload.isMain,
    });
    let specialistRequest = await this.$axios.get(
      `/api/specialists/${payload.specialistId}/`
    );
    if (specialistRequest.status === 200)
      commit("updateSpecialist", specialistRequest.data);
    return res;
  },
  async deleteSpecialistActivity({ commit }, payload) {
    let res = await deleteAxios(
      this.$axios,
      `/api/specialties/${payload.linkId}/`
    );
    let specialistRequest = await this.$axios.get(
      `/api/specialists/${payload.specialistId}/`
    );
    if (specialistRequest.status === 200)
      commit("updateSpecialist", specialistRequest.data);
    return res;
  },

  removeExercises ({ state }, { exercisesIds, specialistsIds }) {
    for (let specialist of state.specialists) {
      if (specialistsIds.includes(specialist.id)) {
        for (let exerciseId of exercisesIds) {
          if (specialist.exercises.includes(exerciseId)) {
            specialist.exercises.splice(specialist.exercises.findIndex(id=>id===exerciseId), 1);
          }
        }
      }
    }
  },
  setExercises ({ state }, { exercisesIds, specialistsIds }) {
    for (let specialist of state.specialists) {
      if (specialistsIds.includes(specialist.id)) {
        for (let exerciseId of exercisesIds) {
          if (!specialist.exercises.includes(exerciseId)) {
            specialist.exercises.push(exerciseId);
          }
        }
      }
    }
  },
};

const mutations = {
  clear(state) {
    state.specialists = [];
    state.fetched = false;
  },
  setSpecialists(state, payload) {
    state.specialists = payload.data;
    state.fetched = payload.success;
  },
  updateSpecialist(state, payload) {
    let specialist = state.specialists.find(
      (specialist) => specialist.id == payload.id
    );
    if (specialist) {
      specialist.activities = payload.activities;
      specialist.hasAdditionalActivity = !!specialist.activities.filter(
        (activity) => !activity.is_main
      ).length;
    }
  },
  setOnlySpecialists(state, payload) {
    state.onlySpecialists = payload;
  },
  setOnlyAdmins(state, payload) {
    state.onlyAdmins = payload;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
