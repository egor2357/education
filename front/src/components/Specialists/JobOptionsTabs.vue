<template>
  <a-spin :spinning="loading">
    <div class="specialist-container">
      <div class="job-options">
        <div class="top-bar">
          <div class="top-bar__side-block">
            <a-button icon="arrow-left" @click="$emit('goBack')">
              Назад
            </a-button>
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
        <div class="job-options__tabs" v-if="filteredActivities.length">
          <a-tabs v-model="activeTab">
            <a-tab-pane
              v-for="activity in filteredActivities"
              :key="activity.id"
            >
              <span slot="tab">
                {{ activity.name }}
              </span>
            </a-tab-pane>
          </a-tabs>
        </div>
        <div class="job-options__cards" v-if="currentActivityOptions.length">
          <div
            class="job-options__card"
            v-for="option in currentActivityOptions"
            :key="option.id"
          >
            <job-option :option="option" />
          </div>
        </div>
        <div v-else>
          <a-empty :image="simpleImage" />
        </div>
      </div>
    </div>
  </a-spin>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import JobOption from "@/components/JobOptions/JobOption";
import { Empty } from "ant-design-vue";
import common from "@/mixins/common";

export default {
  components: {
    JobOption,
  },
  name: "JobOptionsTabs",
  mixins: [common],
  props: {
    currentUser: Object,
  },
  data() {
    return {
      loading: true,
      activeTab: null,
      options: [],
    };
  },
  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },
  async created() {
    let fetches = [];

    if (!this.activitiesFetched) {
      fetches.push(this.fetchActivities());
    }

    fetches.push(this.fetchOptions());

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;

    if (this.filteredActivities.length) {
      this.activeTab = this.filteredActivities[0].id;
    }
  },
  methods: {
    async fetchOptions() {
      try {
        this.loading = true;
        let res = await this.$axios.get(
          `/api/options/?specialist_id=${this.currentUser.id}`
        );
        if (res.status === 200) {
          this.options = res.data;
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

    filteredActivities() {
      return this.activities.filter((item) => {
        return this.currentUser.activitiesId.includes(item.id);
      });
    },

    currentActivityOptions() {
      return this.options.filter((option) => {
        return option.activity_id == this.activeTab;
      });
    },

    currentActivity() {
      return this.filteredActivities.find((activity) => {
        return activity.id == this.activeTab;
      });
    },
  },
};
</script>

<style lang="sass">
.specialist-container
  display: flex
  flex-direction: column
  height: 100%
  overflow: hidden

  .top-bar
    display: flex

  .top-bar__side-block
    flex: 1

.job-options
  display: flex
  flex-direction: column
  height: 100%
  overflow: hidden
  &__header
    display: flex
    flex-direction: row
    align-items: center
    margin-bottom: 10px
    font-size: 16px
    &-filler
      flex: 1
      text-align: right
  &__tabs
    display: flex
    justify-content: center
  &__cards
    display: flex
    flex-direction: column
    flex: 1
    overflow-y: auto
    margin-top: 10px    

  &__card
    position: relative
    padding: 3px
    width: 900px
    margin: 0 auto
</style>
