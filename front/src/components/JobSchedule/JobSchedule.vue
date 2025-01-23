<template>
  <a-spin :spinning="loading">
    <div class="job-schedule">
      <div class="top-bar">
        <div class="top-bar__side-block left">
          <a-button
            :disabled="!remainingSchedule.length"
            class="job-schedule__header__options-fill_button"
            icon="block"
            @click="setForTheWeek"
          >
            Применить шаблон расписания
          </a-button>
        </div>
        <div class="title">Календарь занятий</div>
        <div class="top-bar__side-block right">
          <a-button
            class="job-schedule__header__options-add_button"
            icon="plus"
            @click="openModal(null)"
          >
            Добавить занятие
          </a-button>
        </div>
      </div>

      <div class="job-schedule__interval">
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
            <a :disabled="isWeekCurrent"
              @click.stop.prevent="scheduleToCurrentWeek">К текущей неделе</a>
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
          :checked="isScheduleVisible"
          @change="isScheduleVisible = !isScheduleVisible"
        >
          Показывать шаблон расписания
        </a-checkbox>
      </div>

      <job-modal
        v-if="displayModal"
        :activities="activities"
        :specialists="specialists"
        :editableData="modalEditableData"
        @closeModal="closeModal($event)"
      />
    </div>
  </a-spin>
</template>

<script>
import JobModal from "@/components/JobSchedule/JobModal";
import JobCard from "@/components/JobSchedule/JobCard";
import { mapActions, mapGetters } from "vuex";
import consts from "@/const";
import moment from "moment";
import deleteAxios from "@/middleware/deleteAxios";
import post from "@/middleware/post";

export default {
  components: {
    JobModal,
    JobCard,
  },
  name: "JobSchedule",
  data() {
    return {
      dateFrom: moment(new Date()).weekday(0).toDate(),

      loading: true,

      displayModal: false,
      modalEditableData: null,

      daysOfWeek: consts.daysOfWeek,

      jobs: [],

      isScheduleVisible: true,
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
    isWeekCurrent() {
      return moment(new Date()).weekday(0).isSame(this.momentDateArr[0], 'day');
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

    openModal(job = null) {
      this.modalEditableData = job;
      this.displayModal = true;
    },
    closeModal(jobDate = null) {
      this.displayModal = false;
      let isBetween = moment(jobDate).isBetween(
        this.momentDateArr[0],
        this.momentDateArr[this.momentDateArr.length - 1],
        "day",
        "[]"
      );
      if (jobDate && isBetween) {
        this.fetchJobs();
      }
    },

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
    scheduleToCurrentWeek() {
      this.dateFrom = moment(new Date()).weekday(0).toDate();
      this.fetchJobs();
    },

    async deleteJob(id) {
      try {
        this.loading = true;
        let res = await deleteAxios(this.$axios, `/api/jobs/${id}/`, {});
        if (res.status === 204) {
          this.$message.success("Занятие успешно удалено");
          await this.fetchJobs();
        } else {
          this.$message.error("Произошла ошибка при удалении занятия");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка при удалении занятия");
      } finally {
        this.loading = false;
      }
    },

    async setForTheWeek() {
      try {
        this.loading = true;
        let res = await post(this.$axios, `/api/schedule/set_for_the_week/`, {
          date: this.dateFrom,
        });
        if (res.status === 200) {
          this.$message.success("Занятия по шаблону на неделю успешно созданы");
          await this.fetchJobs();
        } else {
          this.$message.error(
            "Произошла ошибка при создании занятий по шаблону на неделю"
          );
        }
      } catch (e) {
        this.$message.error(
          "Произошла ошибка при создании занятий по шаблону на неделю"
        );
      } finally {
        this.loading = false;
      }
    },
    async setForTheDay(scheduleId, currDateMoment) {
      try {
        this.loading = true;
        let res = await post(
          this.$axios,
          `/api/schedule/${scheduleId}/set_for_the_day/`,
          { date: currDateMoment.toDate() }
        );
        if (res.status === 200) {
          this.$message.success("Занятие по шаблону успешно применено");
          await this.fetchJobs();
        } else {
          this.$message.error(
            "Произошла ошибка при создании занятия по шаблону"
          );
        }
      } catch (e) {
        this.$message.error("Произошла ошибка при создании занятия по шаблону");
      } finally {
        this.loading = false;
      }
    },
    thisDateJobs(currDateMoment) {
      let currDateString = currDateMoment.format("YYYY-MM-DD");
      return this.jobs.filter((job) => {
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
      let jobs = this.thisDateJobs(currDateMoment);

      if (this.isScheduleVisible) {
        let templates = this.thisDayRemainingSchedule(currDateMoment);
        jobs = jobs.concat(templates);
      }

      return jobs.sort((first, second) => {
        return (
          moment(first.start_time, "hh:mm:ss") -
          moment(second.start_time, "hh:mm:ss")
        );
      });

    },
    keydown(event) {
      if (event.type === "keydown" && event.keyCode === 39) {
        this.switchDates(true);
      } else if (event.type === "keydown" && event.keyCode === 37) {
        this.switchDates(false);
      }
    },
  },
};
</script>

<style lang="sass">
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
