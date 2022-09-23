<template>
  <a-spin :spinning="loading">
    <div class="skill-details">
      <div class="top-bar">
        <div class="top-bar__side-block left">
          <a-button icon="left" @click="goBack">Назад</a-button>
        </div>
        <div class="title">Развитие навыка</div>
        <div class="top-bar__side-block right">
          <span class="date-range-label">Период:</span>
          <a-range-picker
            class="date-range-input"
            :value="dateRange"
            @change="dateRangeChange"
            format="DD.MM.YYYY"
            :allowClear="false"
            separator="-"
          />
        </div>
      </div>

      <div class="table-block" v-if="skillReports.length">
        <div class="skill-name">{{ skillReports[0].skill.name }}</div>

        <div class="table-holder">
          <div>
            <div class="table-header">
              <div class="table-cell table-cell_date">
                Дата занятия
                <span
                  class="table-cell-sort"
                  @click="clickedSort('job__date')"
                  :class="{
                    active:
                      activeSort === 'job__date' || activeSort === '-job__date',
                  }"
                >
                  <a-icon
                    type="caret-up"
                    v-if="activeSort === '-job__date'"
                    :class="{ on: activeSort === '-job__date' }"
                  />
                  <a-icon
                    type="caret-down"
                    v-if="activeSort !== '-job__date'"
                    :class="{ on: activeSort === 'job__date' }"
                  />
                </span>
              </div>
              <div class="table-cell table-cell_activity">
                Вид деятельности
                <span
                  class="table-cell-sort"
                  @click="clickedSort('job__activity__name')"
                  :class="{
                    active:
                      activeSort === 'job__activity__name' ||
                      activeSort === '-job__activity__name',
                  }"
                >
                  <a-icon
                    type="caret-up"
                    v-if="activeSort === '-job__activity__name'"
                    :class="{ on: activeSort === '-job__activity__name' }"
                  />
                  <a-icon
                    type="caret-down"
                    v-if="activeSort !== '-job__activity__name'"
                    :class="{ on: activeSort === 'job__activity__name' }"
                  />
                </span>
              </div>
              <div class="table-cell table-cell_specialist">
                Специалист
                <span
                  class="table-cell-sort"
                  @click="clickedSort('job__specialist__surname')"
                  :class="{
                    active:
                      activeSort === 'job__specialist__surname' ||
                      activeSort === '-job__specialist__surname',
                  }"
                >
                  <a-icon
                    type="caret-up"
                    v-if="activeSort === '-job__specialist__surname'"
                    :class="{ on: activeSort === '-job__specialist__surname' }"
                  />
                  <a-icon
                    type="caret-down"
                    v-if="activeSort !== '-job__specialist__surname'"
                    :class="{ on: activeSort === 'job__specialist__surname' }"
                  />
                </span>
              </div>
              <div class="table-cell table-cell_job">Сведения о занятии</div>
            </div>
            <div class="table-body" v-if="skillReports.length">
              <div
                class="table-row"
                v-for="skillReport in skillReports"
                :key="skillReport.id"
                @click="goToJob(skillReport.job)"
              >
                <div class="table-cell table-cell_date">
                  {{ skillReport.job.date | toRuDateString }}
                </div>
                <div class="table-cell table-cell_activity">
                  <div
                    :style="{
                      'background-color': `${skillReport.job.activity.color}10`,
                      border: `1px solid ${skillReport.job.activity.color}99`,
                    }"
                    class="table-cell__activity-name"
                  >
                    {{ skillReport.job.activity.name }}
                  </div>
                </div>
                <div class="table-cell table-cell_specialist">
                  {{
                    skillReport.job.specialist
                      ? skillReport.job.specialist.__str__
                      : ""
                  }}
                </div>
                <div class="table-cell table-cell_job">
                  <div class="table-cell__job">
                    <div class="table-cell__job-topic">
                      {{ skillReport.job.topic }}
                    </div>
                  </div>
                  <div
                    class="table-cell__job-mark"
                    :style="{
                      'background-color': getColorByMark(skillReport.mark),
                    }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <a-empty :image="simpleImage" />
      </div>
    </div>
  </a-spin>
</template>

<script>
import moment from "moment";
import getColorByMark from "@/mixins/getColorByMark";
import { Empty } from "ant-design-vue";

export default {
  name: "SkillDetails",
  mixins: [getColorByMark],
  props: {
    dateRangeInit: {
      type: Array,
      default() {
        return [moment(new Date()).weekday(0), moment(new Date()).weekday(6)];
      },
    },
  },
  data() {
    return {
      loading: true,

      dateRange: [],

      skillReports: [],

      activeSort: "job__date",
    };
  },
  computed: {},
  filters: {
    toRuDateString(value) {
      return moment(value).format("DD.MM.YYYY");
    },
  },
  methods: {
    goBack() {
      this.$router.push({
        name: "AllSkills",
        query: {
          dateFrom: this.$route.query.dateFrom,
          dateTo: this.$route.query.dateTo,
          showCalled: String(this.$route.query.showCalled)
        },
      });
    },
    dateRangeChange(value, replace = false) {
      if (
        value[0].format("YYYY-MM-DD") == this.$route.query.dateFrom &&
        value[1].format("YYYY-MM-DD") == this.$route.query.dateTo
      ) {
        return;
      }

      let queryObj = {
        dateFrom: value[0].format("YYYY-MM-DD"),
        dateTo: value[1].format("YYYY-MM-DD"),
      };

      if (replace) {
        this.$router
          .replace({
            name: this.$route.name,
            query: queryObj,
          })
          .catch(() => {});
      } else {
        this.$router
          .push({
            name: this.$route.name,
            query: queryObj,
          })
          .catch(() => {});
      }
    },
    setDateRange(route) {
      let query = route.query;
      if (
        !Object.prototype.hasOwnProperty.call(query, "dateFrom") ||
        !Object.prototype.hasOwnProperty.call(query, "dateTo")
      ) {
        this.dateRange.splice(0);
        this.dateRange.push(this.dateRangeInit[0].clone());
        this.dateRange.push(this.dateRangeInit[1].clone());
        return false;
      } else {
        this.dateRange.splice(0);
        this.dateRange.push(moment(query.dateFrom, "YYYY-MM-DD"));
        this.dateRange.push(moment(query.dateTo, "YYYY-MM-DD"));
        return true;
      }
    },
    async fetchSkillReports() {
      try {
        this.loading = true;
        let firstQParameter = `date_from=${this.dateRange[0].format(
          "YYYY-MM-DD"
        )}`;
        let secondQParameter = `date_to=${this.dateRange[1].format(
          "YYYY-MM-DD"
        )}`;
        let fourthQParameter = `skill_id=${this.$route.params.id}`;
        let QParameters = `?${firstQParameter}&${secondQParameter}&${fourthQParameter}`;
        let res = await this.$axios.get(
          `/api/skill_reports/${QParameters}&ordering=${this.activeSort}`
        );
        if (res.status === 200) {
          this.skillReports = res.data;
        } else {
          this.$message.error("Произошла ошибка при загрузке отчетов");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка при загрузке отчетов");
      } finally {
        this.loading = false;
      }
    },
    goToJob(job) {
      if (job) {
        this.$router.push({ name: "JobDetails", params: { id: job.id } });
      }
    },
    async clickedSort(param) {
      if (param === "job__date") {
        if (this.activeSort === "job__date") {
          this.activeSort = "-job__date";
        } else if (this.activeSort === "-job__date") {
          this.activeSort = "job__date";
        } else {
          this.activeSort = "job__date";
        }
      } else if (param === "job__activity__name") {
        if (this.activeSort === "job__activity__name") {
          this.activeSort = "-job__activity__name";
        } else if (this.activeSort === "-job__activity__name") {
          this.activeSort = "job__activity__name";
        } else {
          this.activeSort = "job__activity__name";
        }
      } else if (param === "job__specialist__surname") {
        if (this.activeSort === "job__specialist__surname") {
          this.activeSort = "-job__specialist__surname";
        } else if (this.activeSort === "-job__specialist__surname") {
          this.activeSort = "job__specialist__surname";
        } else {
          this.activeSort = "job__specialist__surname";
        }
      }
      await this.fetchSkillReports();
    },
  },

  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },
  async created() {
    if (!this.setDateRange(this.$route)) {
      this.dateRangeChange(this.dateRange, true);
      return;
    }

    this.fetchSkillReports();
  },
  beforeDestroy() {},

  beforeRouteUpdate(to, from, next) {
    if (!this.setDateRange(to)) {
      this.dateRangeChange(this.dateRange, true);
      return;
    }
    this.fetchSkillReports();
    next();
  },
};
</script>

<style lang="sass">
$border-color: #e8e8e8

.skill-details
  display: flex
  flex-direction: column
  overflow: hidden
  height: 100%

  .table-block
    display: flex
    flex-direction: column
    flex: 1
    overflow: hidden

  .top-bar
    display: flex
    line-height: 32px

    .title
      font-size: 1rem
      text-align: center
      margin: 0 10px

  .top-bar__side-block
    flex: 1

    &.right
      text-align: right
      white-space: nowrap

    .date-range-label
      margin-right: 10px

    .date-range-input
      width: 220px
      text-align: center

  .skill-name
    max-width: 900px
    text-align: center
    margin: 0 auto 10px
    font-size: 20px
    line-height: 32px

  .table-holder
    overflow: auto
    flex: 1

  .table-header
    display: flex
    align-items: center
    background: #fafafa
    border: 1px solid $border-color
    overflow: hidden
    line-height: 15px
    z-index: 1
    position: sticky
    position: -webkit-sticky
    top: 0

  .table-cell
    padding: 10px 15px
    display: flex
    align-items: center
    min-height: 52px
    word-break: break-word

    &-sort
      margin: 5px 0 0 5px
      color: #bfbfbf
      display: none
      .anticon-caret-up, .anticon-caret-down
        font-size: 15px
        cursor: pointer
        &.on
          color: #1890ff
      &.active
        display: unset
    &:hover
      .table-cell-sort
        display: unset

  .table-cell_date
    width: 150px

  .table-cell_activity
    width: 200px
    border-left: 1px solid $border-color

  .table-cell_specialist
    width: 200px
    border-left: 1px solid $border-color

  .table-cell_job
    flex: 1
    border-left: 1px solid $border-color

  .table-body
    border: 1px solid $border-color
    border-top: 0 none

  .table-row
    display: flex

  .table-row
    border-top: 1px solid $border-color
    cursor: pointer

  .table-row:first-child
    border-top: 0 none

  .table-row:hover
    background: #e6f7ff

  .table-cell__activity-name
    padding: 2px 5px
    border-radius: 4px
    flex: 1
    text-align: center


  .table-cell__job
    display: flex
    flex-direction: row
    flex: 1
    min-width: 200px
    padding: 0 15px 0 0

    &-text
      display: flex
      flex-direction: row
      flex: 1
    &-mark
      height: 26px
      width: 26px
      border-radius: 13px
      box-shadow: 0 1px 3px 1px #dedede
    &-topic
      margin-right: 10px
      font-weight: bold
</style>
