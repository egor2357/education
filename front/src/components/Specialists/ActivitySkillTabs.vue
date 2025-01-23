<template>
  <div class="specialist-container">
    <div class="top-bar">
      <div class="top-bar__side-block">
        <a-button icon="arrow-left" @click="$emit('goBack')">Назад</a-button>
      </div>
      <span class="specialist-title">
        <span>Виды деятельности специалиста:</span>
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

    <div class="specialist-tab-content">
      <ActivitiesTypes
        :userActivities="currentUser.activities"
        :specialistId="currentUser.id"
      />
    </div>
  </div>
</template>

<script>
import ActivitiesTypes from "@/components/Specialists/ActivitiesTypes";
import common from "@/mixins/common";
export default {
  name: "ActivitySkillTabs",
  components: {
    ActivitiesTypes,
  },
  mixins: [common],
  props: {
    currentUser: Object,
  },
  data() {
    return {
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

.specialist-tab-content
  flex: 1
  overflow: hidden
</style>
