<template>
  <a-spin :spinning="loading">
    <div class="job-schedule-wrapper">
      <div class="top-bar">
        <div class="title">Занятия</div>
      </div>
      <AvailableChart
        :specReadOnly="true"
        :userId="userInfo.id"
        ref="available-read-only"
      />

      <div class="job-schedule">
        <div class="job-schedule__interval job-schedule__interval--small">
          <a-icon
            class="icon-button job-schedule__interval-shift job-schedule__interval-shift_left"
            type="left"
            @click="switchDates(false)"
          />
          <div class="job-schedule__interval-center">
            <div class="job-schedule__interval-label">
              <div class="job-schedule__interval-item">
                <div class="job-schedule__interval-date">{{ startIntervalFormattedDate.date }}</div>
                <div class="job-schedule__interval-year">{{ startIntervalFormattedDate.year }}</div>
              </div>
              <div class="job-schedule__interval-divider">-</div>
              <div class="job-schedule__interval-item">
                <div class="job-schedule__interval-date">{{ endIntervalFormattedDate.date }}</div>
                <div class="job-schedule__interval-year">{{ endIntervalFormattedDate.year }}</div>
              </div>
            </div>

            <div class="job-schedule__interval-link">
              <a @click.stop.prevent="scheduleToCurrentWeek">К текущей неделе</a>
            </div>
          </div>
          <a-icon
            class="icon-button job-schedule__interval-shift job-schedule__interval-shift_right"
            type="right"
            @click="switchDates(true)"
          />
        </div>

        <div class="job-schedule__calendar">
          <div class="job-schedule__calendar__week">
            <div
              class="job-schedule__calendar__date"
              v-for="(weekday, index) in momentDateArr"
              :key="index"
            >
              <div
                class="job-schedule__calendar__date-title"
                :class="{ weekend: weekday.isoWeekday() > 5 }"
              >
                <div class="job-schedule__calendar__date-title-day">
                  <div>
                    {{ weekday.format("D") }}
                  </div>
                  <div>
                    {{ weekday.format("D MMMM").split(" ")[1] }}
                  </div>
                </div>
                <div class="job-schedule__calendar__date-title-weekday">
                  {{ weekday.format("dd").toUpperCase() }}
                </div>
              </div>
              <div class="job-schedule__calendar__jobs">
                <a-timeline>
                  <template
                    v-for="(item, index) in thisDateJobsNSchedule(weekday)"
                  >
                    <a-timeline-item
                      v-if="'schedule' in item"
                      :key="index"
                      :color="item.activity.color"
                    >
                      <a-icon v-if="item.filled_reports_count"
                        slot="dot" type="check-circle"
                        :style="'color:'+item.activity.color"/>
                      <job-card
                        :job="item"
                        @deleteJob="deleteJob($event)"
                        @editJob="openModal($event)"
                        :readOnly="true"
                      >
                      </job-card>
                    </a-timeline-item>
                    <a-timeline-item v-else :key="index" :color="'#ccc'">
                      <div class="job-schedule__calendar__template">
                        <div class="job-schedule__calendar__template-time">
                          {{ item.start_time.substr(0, 5) }}
                        </div>
                        <div
                          class="job-schedule__calendar__template-activity-name"
                        >
                          {{ item.activity.name }}
                        </div>
                        <div class="job-schedule__calendar__template-overlay">
                          <a-button
                            type="primary"
                            class="job-schedule__calendar__template-overlay__button"
                            @click="setForTheDay(item.id, weekday)"
                          >
                            Применить
                          </a-button>
                        </div>
                      </div>
                    </a-timeline-item>
                  </template>
                </a-timeline>
              </div>
            </div>
          </div>
        </div>

        <div>
          <a-checkbox
            class="job-schedule__switcher"
            v-model="showOnlyMyJobs"
          >
            Показывать только мои занятия
          </a-checkbox>
        </div>
      </div>
    </div>
  </a-spin>
</template>

<script>
import JobCard from "@/components/JobSchedule/JobCard";
import { mapActions, mapGetters } from "vuex";
import consts from "@/const";
import moment from "moment";
import AvailableChart from "@/views/Admin/AvailableChart";

export default {
  components: {
    JobCard,
    AvailableChart,
  },
  name: "ScheduleReadOnly",
  data() {
    return {
      dateFrom: moment(new Date()).weekday(0).toDate(),

      loading: true,

      displayModal: false,
      modalEditableData: null,

      daysOfWeek: consts.daysOfWeek,

      showOnlyMyJobs: false,

      jobs: [],
    };
  },

  computed: {
    ...mapGetters({
      specialists: "specialists/getSpecialists",
      specialistsFetched: "activities/getFetched",
      activities: "activities/getActivities",
      activitiesFetched: "activities/getFetched",
      schedule: "schedule/getJobs",
      scheduleFetched: "schedule/getFetched",
      userInfo: "auth/getUserInfo",
      selectedDay: "schedule/getSelectedDay",
    }),

    momentDateArr() {
      let momentFrom = moment(this.dateFrom).clone().weekday(0);
      let currMoment = momentFrom.clone();
      let momentTo = currMoment.clone().weekday(6);

      let dateArray = [];
      while (currMoment <= momentTo) {
        dateArray.push(currMoment.clone());
        currMoment = currMoment.add(1, "days");
      }
      return dateArray;
    },
    startIntervalFormattedDate() {
      let date = this.momentDateArr[0];
      return {date: date.format("D MMMM"), year: date.format("YYYY")};
    },
    endIntervalFormattedDate() {
      let date = this.momentDateArr[this.momentDateArr.length - 1];
      return {date: date.format("D MMMM"), year: date.format("YYYY")};
    },
    jobSheduleIndexes() {
      return this.jobs.map((job) => {
        if (job.schedule) {
          return job.schedule.id;
        }
      });
    },
    remainingSchedule() {
      return this.schedule.filter((schedule) => {
        return !this.jobSheduleIndexes.includes(schedule.id);
      });
    },
  },

  async created() {
    let fetches = [];

    if (this.selectedDay) {
      this.dateFrom = moment(this.selectedDay).weekday(0).toDate();
    }

    if (!this.activitiesFetched) {
      fetches.push(this.fetchActivities());
    }
    if (!this.specialistsFetched) {
      fetches.push(this.fetchSpecialists());
    }
    if (!this.scheduleFetched) {
      fetches.push(this.fetchSchedule());
    }

    fetches.push(this.fetchJobs());

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;
    document.addEventListener("keydown", this.keydown);
  },
  beforeDestroy() {
    document.removeEventListener("keydown", this.keydown);
  },

  methods: {
    ...mapActions({
      fetchSpecialists: "specialists/fetchSpecialists",
      fetchActivities: "activities/fetchActivities",
      fetchSchedule: "schedule/fetchJobs",
    }),

    async fetchJobs() {
      try {
        this.loading = true;
        let firstQParameter = `date__gte=${this.momentDateArr[0].format(
          "YYYY-MM-DD"
        )}`;
        let secondQParameter = `date__lte=${this.momentDateArr[
          this.momentDateArr.length - 1
        ].format("YYYY-MM-DD")}`;
        let res = await this.$axios.get(
          `/api/jobs/?${firstQParameter}&${secondQParameter}`
        );
        if (res.status === 200) {
          this.jobs = res.data;
        } else {
          this.$message.error("Произошла ошибка при загрузке занятий");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка при загрузке занятий");
      } finally {
        this.loading = false;
      }
    },

    switchDates(isForward) {
      let newMomentFrom = moment(this.dateFrom);
      if (isForward) {
        newMomentFrom = newMomentFrom.add(7, "days");
      } else {
        newMomentFrom = newMomentFrom.subtract(7, "days");
      }
      this.dateFrom = newMomentFrom.toDate();
      this.fetchJobs();
    },

    thisDateJobs(currDateMoment) {
      let currDateString = currDateMoment.format("YYYY-MM-DD");
      let jobs = this.jobs;
      let userId = this.userInfo.specialistId;

      if (this.showOnlyMyJobs) {
        jobs = jobs.filter((job)=>{
          return job.specialist && job.specialist.id == userId;
        });
      }

      return jobs.filter((job) => {
        return job.date == currDateString;
      });
    },
    thisDayRemainingSchedule(currDateMoment) {
      let day = currDateMoment.weekday();
      return this.remainingSchedule.filter((schedule) => {
        return schedule.day == day;
      });
    },
    thisDateJobsNSchedule(currDateMoment) {
      return this.thisDateJobs(currDateMoment).sort((first, second) => {
        return (
          moment(first.start_time, "hh:mm:ss") -
          moment(second.start_time, "hh:mm:ss")
        );
      });
    },
    async keydown(event) {
      if (
        event.type === "keydown" &&
        (event.keyCode === 39 || event.keyCode === 37)
      ) {
        let oldStart = this.dateFrom;
        if (event.keyCode === 39) {
          await this.switchDates(true);
        } else {
          await this.switchDates(false);
        }
        let newStart = this.dateFrom;
        if (
          newStart.getMonth() !== oldStart.getMonth() &&
          this.$refs["available-read-only"].currentDate.month() !== newStart &&
          event.keyCode === 39
        ) {
          this.$refs["available-read-only"].currentDate = moment(oldStart);
          this.$refs["available-read-only"].changeMonth(true);
        }
        if (
          newStart.getMonth() !== oldStart.getMonth() &&
          this.$refs["available-read-only"].currentDate.month() !==
            newStart.getMonth() &&
          event.keyCode === 37
        ) {
          this.$refs["available-read-only"].currentDate = moment(oldStart);
          this.$refs["available-read-only"].changeMonth(false);
        }
      }
    },

    scheduleToCurrentWeek() {
      this.dateFrom = moment(new Date()).weekday(0).toDate();
      this.fetchJobs();
    },

  },
};
</script>

<style lang="sass">
.job-schedule-wrapper
  height: 100%
  display: flex
  flex-direction: column
  .top-bar
    line-height: 32px
    text-align: center
    .title
      font-size: 1rem

.job-schedule
  &__interval-label
    display: flex
    flex-direction: row
    align-items: center
    padding: 0px 10px
  &__interval-item
    display: flex
    flex-direction: column
    flex-grow: 1
    align-items: center
  &__interval-divider
    margin: 0px 6px
    padding-top: 3px
    color: #ccc
  &__interval-date
  &__interval-year
    width: 100%
    border-top: 1px solid #ccc
    font-size: 14px

  &__interval-link
    font-size: 13px
    text-align: center
</style>
