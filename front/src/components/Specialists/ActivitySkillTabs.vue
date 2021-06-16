<template>
  <div class="specialist-container">
    <div class="top-bar">
      <div class="top-bar__side-block">
        <a-button icon="arrow-left" @click="$emit('goBack')">Назад</a-button>
      </div>
      <span class="specialist-title">
        <span>Специалист:</span>
        <b>
          {{
            currentUser.surname
              ? formatSpecialistFull(currentUser)
              : currentUser.user.username
          }}
        </b>
      </span>
      <div class="top-bar__side-block"></div>
    </div>
    <div class="specialist-tabs-container">
      <a-tabs v-model="activeTab">
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
    </div>
    <div class="specialist-tab-content">
      <ActivitiesTypes
        v-show="activeTab == 1"
        :userActivities="currentUser.activities"
        :specialistId="currentUser.id"
      />
      <Skills
        :specialistSkills="currentUser.skills"
        :specialistId="currentUser.id"
        v-show="activeTab == 2"
      />
    </div>
  </div>
</template>

<script>
import ActivitiesTypes from "@/components/Specialists/ActivitiesTypes";
import Skills from "@/components/Specialists/Skills";
import common from "@/mixins/common";
export default {
  name: "ActivitySkillTabs",
  components: {
    ActivitiesTypes,
    Skills,
  },
  mixins: [common],
  props: {
    currentUser: Object,
  },
  data() {
    return {
      activeTab: "1",
    };
  },
};
</script>

<style lang="sass">
.specialist-container
  display: flex
  flex-direction: column
  flex: 1
  overflow: hidden

  .top-bar
    display: flex

  .top-bar__side-block
    flex: 1

.specialist-title
  text-align: center

.specialist-tabs-container
  display: flex
  justify-content: center

.specialist-tab-content
  flex: 1
  overflow: hidden
</style>
