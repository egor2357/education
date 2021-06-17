<template>
  <a-spin :spinning="loading">
    <div class="job-options">
      <div class="job-options__header">Планы занятий</div>
      <div class="job-options__tabs">
        <a-tabs v-model="activeTab">
          <a-tab-pane v-for="activity in activities" :key="activity.id">
            <span slot="tab">
              {{ activity.name }}
            </span>
          </a-tab-pane>
        </a-tabs>
      </div>

    </div>
  </a-spin>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  components: {
  },
  name: "JobOptions",
  data() {
    return {
      loading: true,

      activeTab: null,

    };
  },
  async created() {
    let fetches = []

    if (!this.activitiesFetched) {
      fetches.push(this.fetchActivities());
    }

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;

    if (this.activities.length) {
      this.activeTab = this.activities[0].id;
    }

  },
  methods: {
    // async fetchUserData(){
    //   try {
    //     this.loading = true;
    //     let res = await this.$axios.get("/api/users/current");
    //     if (res.status === 200) {
    //       this.userData = res.data;
    //     } else if (res.status === 400) {
    //       this.$message.error("Ошибка при загрузке данных специалиста");
    //     } else {
    //       this.$message.error("Ошибка при загрузке данных специалиста");
    //     }
    //   } catch (e) {
    //     this.$message.error("Ошибка при загрузке данных специалиста");
    //   } finally {
    //     this.loading = false;
    //   }
    // },

    ...mapActions({
      fetchActivities: "activities/fetchActivities",
    }),
  },
  computed: {
    ...mapGetters({
      activitiesFetched: "activities/getFetched",
      activities: "activities/getActivities",
    }),
  },
};
</script>

<style lang="sass">
  .job-options
    display: flex
    flex-direction: column
    height: 100%
    overflow: hidden
    &__header
      text-align: center
      font-size: 16px
      margin-bottom: 10px
    &__tabs
      display: flex
      justify-content: center
</style>
