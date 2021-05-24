<template>
  <div>
    <div style="display: flex">
      <a-button icon="arrow-left" @click="$emit('goBack')">Назад</a-button>
      <span class="specialist-title">
        <span>Специалист:</span>
        <b>
          {{
            currentUser.surname
              ? currentUser.name && currentUser.patronymic
                ? `${currentUser.surname} ${currentUser.name} ${currentUser.patronymic}`
                : currentUser.surname
              : currentUser.user.username
          }}
        </b>
      </span>
    </div>
    <a-tabs v-model="activeTab" class="specialist-tabs--center">
      <a-tab-pane key="1">
        <span slot="tab">
          <a-icon type="unordered-list" />
          Виды деятельности
        </span>
      </a-tab-pane>
      <a-tab-pane key="2">
        <span slot="tab">
          <a-icon type="share-alt" />
          Навыки
        </span>
      </a-tab-pane>
    </a-tabs>
    <ActivitiesTypes
      v-show="activeTab == 1"
      :activities="activities"
      :userActivities="currentUser.activities"
      :specialistId="currentUser.id"
    />
    <Skills
      :specialistSkills="currentUser.skills"
      :specialistId="currentUser.id"
      v-show="activeTab == 2"
    />
  </div>
</template>

<script>
import ActivitiesTypes from "@/components/Specialists/ActivitiesTypes";
import Skills from "@/components/Specialists/Skills";
import { mapActions, mapGetters } from "vuex";
export default {
  name: "ActivitySkillTabs",
  components: {
    ActivitiesTypes,
    Skills,
  },
  props: {
    currentUser: Object,
  },
  data() {
    return {
      activeTab: "1",
      loadingList: true,
    };
  },
  async created() {
    await this.fetchActivities();
    this.loadingList = false;
  },
  methods: {
    ...mapActions({
      fetchActivities: "activities/fetchActivities",
    }),
  },
  computed: {
    ...mapGetters({
      activities: "activities/getActivities",
    }),
  },
};
</script>

<style lang="sass">
.specialist-title
  flex-grow: 1
  text-align: center
  padding-right: 7%
.specialist-tabs--center
  padding-right: calc(50% - 160px)
  padding-left: calc(50% - 160px)
</style>
