<template>
  <div class="job-details job-details--read-only">
    <div class="job-details__header">
      <div class="job-details__header-title">
        <div class="job-details__header-left-block">
          <a-button icon="left" @click="$router.go(-1)">Назад</a-button>
        </div>
        <div class="job-details__header-center-block" v-if="job">
          <div class="job-details__header-title__activity">
            <div
              :style="{
                'background-color': `${job.activity.color}10`,
                border: `1px solid ${job.activity.color}99`,
              }"
            >
              {{ job.activity.name }}
            </div>
          </div>
          <div class="job-details__header-title__date">
            <div class="job-details__header-title__date-time">
              {{ job.start_time.substr(0, 5) }}
            </div>
            <div class="job-details__header-title__date-day">
              {{ jobDateMoment.format("D MMMM") }}
            </div>
            <div class="job-details__header-title__date-weekday">
              {{ jobDateMoment.format("dddd") }}
            </div>
          </div>
          <div class="job-details__header-title__specialist">
            <div class="job-details__header-title__specialist-label">
              Специалист:
            </div>
            <div class="job-details__header-title__specialist-name">
              {{ job.specialist ? job.specialist.__str__ : "Не назначен" }}
            </div>
          </div>
        </div>
        <div class="job-details__header-right-block" />
      </div>
    </div>

    <div class="job-details__content">
      <div class="job-details__tabs-holder">
        <a-tabs v-model="activeTab" class="job-details__tabs">
          <a-tab-pane key="1">
            <span slot="tab">
              <a-icon type="setting" />
              Параметры занятия
            </span>
          </a-tab-pane>
          <a-tab-pane key="2">
            <span slot="tab">
              <a-icon type="carry-out" />
              Отчет
            </span>
          </a-tab-pane>
        </a-tabs>
      </div>
      <div class="job-details__tab_content">
        <JobOption :option="job" v-if="activeTab == 1" />

        <div v-if="activeTab == 2" class="job-details__wrapper">
          <template v-if="reportForm.marks.length">
            <div class="job-details__label">Уровень освоения</div>
            <div class="job-details__reports">
              <div
                class="job-details__report"
                v-for="report in reportForm.marks"
                :key="report.id"
              >
                <div class="job-details__report-name">
                  {{ `${report.exercise.area_number}.${report.exercise.direction_number}.${report.exercise.skill_number}.${report.exercise.number}. ${report.exercise.name}` }}
                </div>
                <div class="job-details__report-marks">
                  <div
                    class="job-details__report-mark"
                    v-for="i in 3"
                    :key="i"
                    :class="{ current: report.mark == i - 1 }"
                    :style="{ 'background-color': getColorByMark(i - 1) }"
                  ></div>
                </div>
              </div>
            </div>
          </template>
          <div class="job-details__report__no-data" v-else>
            <a-empty :image="simpleImage" />
          </div>
          <div
            v-if="reportForm.report_comment"
            class="job-details__report-comment"
          >
            <div class="job-details__report-comment-title">
              Результат проведения занятия:
            </div>
            <div class="job-details__report-comment-text">
              {{ reportForm.report_comment }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import JobOption from "@/components/JobOptions/JobOption";
import moment from "moment";
import getColorByMark from "@/mixins/getColorByMark";
import { Empty } from "ant-design-vue";
export default {
  name: "JobReadOnly",
  components: {
    JobOption,
  },
  props: {
    job: {
      type: Object,
      default: null,
    },
  },
  mixins: [getColorByMark],
  data() {
    return {
      jobDateMoment: moment(this.job.date, "YYYY-MM-DD"),
      activeTab: "1",
      reportForm: {
        marks: [],
        report_comment: "",
      },
    };
  },
  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },
  created() {
    this.reportForm.marks = this.job.reports.slice();
    this.reportForm.report_comment = this.job.report_comment;
    this.$store.commit("schedule/setSelectedDay", this.job.date);
  },
};
</script>

<style lang="sass">
.job-details--read-only
  .job-details__tab_content
    padding: 0 20%

  .job-details__reports
    max-height: 550px

  .job-details__report-mark:hover
    cursor: default
    &:not(.current)
      opacity: 0.2


  .job-details__report-comment
    width: 100%
    &-title
      font-weight: bold

  .job-details__wrapper
    padding: 0
.job-details__report__no-data
  display: flex
  flex-direction: column
  align-items: center
  width: 100%
</style>
