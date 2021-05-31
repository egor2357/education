import post from "@/middleware/post";
import put from "@/middleware/put";
import deleteAxios from "@/middleware/deleteAxios";

const state = () => ({
  activities: [],
  activitiesCheckboxes: {},
  fetched: false,
});

const getters = {
  getFetched(state) {
    return state.fetched;
  },
  getActivities(state) {
    return state.activities;
  },
  getActivitiesCheckboxes(state) {
    return state.activitiesCheckboxes;
  },
};

const actions = {
  async fetchActivities({commit}) {
    try {
      let res = await this.$axios.get("/api/activities/");
      if (res.status === 200) {
        commit("setActivities", res.data);
      }
    }
    catch (e) {
      commit("setActivities", []);
    }
  },
  async addActivity(context, payload) {
    return post(this.$axios, "/api/activities/", payload);
  },
  async editActivity(context, payload) {
    return put(this.$axios, `/api/activities/${payload.id}/`, payload);
  },
  async deleteActivity(context, id) {
    return deleteAxios(this.$axios, `/api/activities/${id}/`, {});
  },
  async addLinkSkill(context, payload) {
    return put(this.$axios, `/api/activities/${payload.activityId}/skills/`, {skill_id: payload.skillId});
  },
  async deleteLinkSkill(context, payload) {
    return deleteAxios(this.$axios, `/api/activities/${payload.activityId}/skills/`, {skill_id: payload.skillId});
  }
};

const mutations = {
  setActivities(state, payload) {
    state.activities = payload;
    state.fetched = true;
  },
  setActivitiesCheckboxes(state, payload) {
    state.activitiesCheckboxes = payload;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
