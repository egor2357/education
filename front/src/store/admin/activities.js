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
        commit("setActivities", {data: res.data, success: true});
      }
    }
    catch (e) {
      commit("setActivities", {data: [], success: false});
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
  async addLinkSkill({commit}, payload) {
    let res = await put(this.$axios, `/api/activities/${payload.activityId}/skills/`, {skill_id: payload.skillId});
    if (res.status === 200)
      commit("updateActivitySkills", {activityId: payload.activityId, skills: res.data.skills});
    return res;
  },
  async deleteLinkSkill({commit}, payload) {
    let res = await deleteAxios(this.$axios, `/api/activities/${payload.activityId}/skills/`, {skill_id: payload.skillId});
    if (res.status === 200)
      commit("updateActivitySkills", {activityId: payload.activityId, skills: res.data.skills});
    return res;
  }
};

const mutations = {
  setActivities(state, payload) {
    state.activities = payload.data;
    state.fetched = payload.success;
  },
  setActivitiesCheckboxes(state, payload) {
    state.activitiesCheckboxes = payload;
  },
  updateActivitySkills(state, payload)
  {
    let activity = state.activities.find(activity => activity.id == payload.activityId);
    if (activity)
      activity.skills = payload.skills;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
