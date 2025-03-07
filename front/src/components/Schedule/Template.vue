<template>
  <div style="overflow: auto; flex: 1;">
    <div class="schedule-week">
      <div class="day" v-for="index in [0, 1, 2, 3, 4, 5, 6]" :key="index">
        <div class="title">
          {{ daysOfWeek[index].long }}
        </div>
        <div class="jobs">
          <a-timeline>
            <template v-for="job in jobs">
              <a-timeline-item
                :color="job.activity.color"
                v-if="index === job.day"
                :key="job.id"
              >
                <div
                  class="job-card"
                  :style="{
                    'background-color': `${job.activity.color}4d`,
                    border: `1px solid ${job.activity.color}99`,
                  }"
                >
                  <div class="job-time">{{ formatTime(job.start_time) }}</div>
                  <a-dropdown
                    :trigger="['click']"
                    placement="bottomLeft"
                    class="dropdown--hover"
                  >
                    <a-icon class="icon-button" type="more"></a-icon>
                    <a-menu slot="overlay">
                      <a-menu-item key="1" @click="openModalEdit(job)">
                        Изменить
                      </a-menu-item>
                      <a-menu-item
                        key="2"
                        @click="displayConfirmDelete(job, index)"
                      >
                        <span> Удалить </span>
                      </a-menu-item>
                    </a-menu>
                  </a-dropdown>
                  <div class="job-name">{{ job.activity.name }}</div>
                </div>
              </a-timeline-item>
            </template>
          </a-timeline>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import consts from "@/const";
import { mapGetters, mapActions } from "vuex";
import datetime from "@/mixins/datetime";
export default {
  name: "Template",
  mixins: [datetime],
  data() {
    return {
      daysOfWeek: consts.daysOfWeek,
    };
  },
  async created() {
    this.$emit("startLoading");
    await this.fetchJobs();
    this.$emit("endLoading");
  },
  methods: {
    ...mapActions({
      fetchJobs: "schedule/fetchJobs",
      deleteJob: "schedule/deleteJob",
    }),
    displayConfirmDelete({ id, activity, start_time }, index) {
      let that = this;
      this.$confirm({
        title: `Занятие "${activity.name}" (${
          this.daysOfWeek[index].long
        }, ${this.formatTime(start_time)}) будет удалено.`,
        content: "Продолжить?",
        okType: "danger",
        onOk() {
          that.deleteRecord(id);
        },
      });
    },
    async deleteRecord(id) {
      try {
        this.$emit("startLoading");
        let res = await this.deleteJob(id);
        if (res.status === 204) {
          this.$message.success("Занятие успешно удалено из шаблона");
          await this.fetchJobs();
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      } finally {
        this.$emit("endLoading");
      }
    },
    openModalEdit(job) {
      this.$emit("openModalEdit", job);
    },
  },
  computed: {
    ...mapGetters({
      jobs: "schedule/getJobs",
    }),
  },
};
</script>

<style lang="sass">
.schedule-week
  display: flex
  flex-direction: row
  min-height: 100%
  .day
    flex: 1 1 auto
    border-right: 1px solid #D9D9D9
    border-bottom: 1px solid #D9D9D9
    min-width: 150px
    max-width: 250px
    &:first-child
      border-left: 1px solid #D9D9D9
    .title
      text-align: center
      border-bottom: 1px solid #D9D9D9
      background-color: #FF8D74
      padding: 10px
      color: #FFFFFF
      font-size: 1rem
      position: sticky
      position: -webkit-sticky
      top: 0
      z-index: 3
    .jobs
      padding: 15px 10px 10px 5px
      .job-card
        padding: 10px
        border-radius: 4px
        display: flex
        flex-wrap: wrap
        .job-time
          flex: 0 0 95%
        .dropdown--hover
          display: none
          max-width: 0
          height: 20px
        &:hover
          cursor: pointer
          box-shadow: 0 0 2px 1px rgba(0,0,0,.15)
          .dropdown--hover
            display: unset
        .icon-button
            font-size: 16px
        .job-name
          flex: 0 0 100%
</style>
