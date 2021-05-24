<template>
  <div>
    <a-tabs v-model="activeTab" class="tabs--center">
      <a-tab-pane key="1">
        <span slot="tab">
          <a-icon type="unordered-list" />
          Список
        </span>
      </a-tab-pane>
      <a-tab-pane key="2">
        <span slot="tab">
          <a-icon type="share-alt" />
          Вид деятельности / навыки
        </span>
      </a-tab-pane>
    </a-tabs>
    <TypesList
      v-if="activeTab == 1"
      :data="activities"
      @needUpdate="fetchActivities"
      :loadingList="loadingList"
    />
    <ActivitiesSkills
      v-if="activeTab == 2"
    />
  </div>
</template>

<script>
import TypesList from "@/components/ActivitiesTypes/TypesList";
import ActivitiesSkills from "@/components/ActivitiesTypes/ActivitiesSkills";
import { mapActions, mapGetters } from "vuex";
export default {
  name: "ActivitiesTypes",
  components: {
    TypesList,
    ActivitiesSkills
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
.tabs--center
  padding-right: calc(50% - 185px)
  padding-left: calc(50% - 185px)
</style>
