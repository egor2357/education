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
      <div>
        <div v-for="option in currentActivityOptions" :key="option.id">
          <job-option :option="option"/>
        </div>
      </div>

    </div>
  </a-spin>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import JobOption from "@/components/JobOptions/JobOption";

export default {
  components: {
    JobOption
  },
  name: "JobOptions",
  data() {
    return {
      loading: true,

      activeTab: null,

      options: [],

    };
  },
  async created() {
    let fetches = []

    if (!this.activitiesFetched) {
      fetches.push(this.fetchActivities());
    }

    fetches.push(this.fetchOptions());

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;

    if (this.activities.length) {
      this.activeTab = this.activities[0].id;
    }

  },
  methods: {
    async fetchOptions(){
      try {
        this.loading = true;
        let res = await this.$axios.get("/api/options");
        if (res.status === 200) {
          this.options = res.data;
        } else if (res.status === 400) {
          this.$message.error("Ошибка при загрузке планов занятий специалиста");
        } else {
          this.$message.error("Ошибка при загрузке планов занятий специалиста");
        }
      } catch (e) {
        this.$message.error("Ошибка при загрузке планов занятий специалиста");
      } finally {
        this.loading = false;
      }
    },

    ...mapActions({
      fetchActivities: "activities/fetchActivities",
    }),
  },
  computed: {
    ...mapGetters({
      activitiesFetched: "activities/getFetched",
      activities: "activities/getActivities",
    }),

    currentActivityOptions(){
      return this.options.filter((option)=>{
        return option.activity_id == this.activeTab;
      })
    }
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
