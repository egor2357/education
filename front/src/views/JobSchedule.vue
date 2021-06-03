<template>
  <a-spin :spinning="loading">
    <div class="job-schedule">

      <div class="job-schedule__header">

        <div class="job-schedule__header-title">
          Календарь занятий
        </div>

        <div class="job-schedule__header__options">
          <div class="job-schedule__header__options-navigate">
            <a-icon class="icon-button job-schedule__header__options-navigate-to_left"
              type="left" @click="switchDates(false)"/>
            <div class="job-schedule__header__options-navigate-interval">
              {{dateIntervalString}}
            </div>
            <a-icon class="icon-button job-schedule__header__options-navigate-to_right"
            type="right" @click="switchDates(true)"/>
          </div>
          <a-button class="job-schedule__header__options-fill_button"
            icon="block" @click="setForTheWeek">
            Применить шаблон расписания
          </a-button>
          <a-button class="job-schedule__header__options-add_button"
            icon="plus" @click="openModal(null)">
            Добавить занятие
          </a-button>
        </div>

      </div>

      <div class="job-schedule__calendar">
        <div class="job-schedule__calendar__week">
          <div class="job-schedule__calendar__date" v-for="weekday, index in momentDateArr" :key="index">
            <div class="job-schedule__calendar__date-title">
              <div class="job-schedule__calendar__date-title-day">
                <div>
                  {{ weekday.format("D") }}
                </div>
                <div>
                  {{ weekday.format("MMM") }}
                </div>
              </div>
              <div class="job-schedule__calendar__date-title-weekday">
                  {{ weekday.format("dd").toUpperCase() }}
              </div>
            </div>
            <div class="job-schedule__calendar__jobs">
              <a-timeline>
                <a-timeline-item v-for="job in thisDateJobs(weekday.format('YYYY-MM-DD'))"
                  :color="job.activity.color"
                  :key="job.id">
                  <job-card :job="job"
                    @deleteJob="deleteJob($event)"
                    @editJob="openModal($event)">

                  </job-card>
                </a-timeline-item>
              </a-timeline>
            </div>
          </div>
        </div>
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
// import post from "@/middleware/post";

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
    };
  },
  async created() {
    let fetches = []

    if (!this.activitiesFetched) {
      fetches.push(this.fetchActivities());
    }
    if (!this.specialistsFetched) {
      fetches.push(this.fetchSpecialists());
    }
    fetches.push(this.fetchJobs())

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;

  },
  methods: {
    ...mapActions({
      fetchSpecialists: "specialists/fetchSpecialists",
      fetchActivities: "activities/fetchActivities",
    }),

    openModal(job=null) {
      this.modalEditableData = job;
      this.displayModal = true;
    },
    closeModal(jobDate=null){
      this.displayModal = false;
      let isBetween = moment(jobDate).isBetween(
        this.momentDateArr[0],
        this.momentDateArr[this.momentDateArr.length-1],
        undefined,
        "[]"
      );
      if (jobDate && isBetween) {
        this.fetchJobs();
      }
    },

    async fetchJobs(){
      try {
        this.loading = true;
        let firstQParameter = `date__gte=${this.momentDateArr[0].format("YYYY-MM-DD")}`;
        let secondQParameter = `date__lte=${this.momentDateArr[this.momentDateArr.length-1].format("YYYY-MM-DD")}`;
        let res = await this.$axios.get(`/api/jobs/?${firstQParameter}&${secondQParameter}`);
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

    switchDates(isForward){
      let newMomentFrom = moment(this.dateFrom);
      if (isForward) {
        newMomentFrom = newMomentFrom.add(7, 'days');
      } else {
        newMomentFrom = newMomentFrom.subtract(7, 'days');
      }
      this.dateFrom = newMomentFrom.toDate();
      this.fetchJobs();
    },

    async deleteJob(id){
      console.log(id);
      // try {
      //   this.loading = true;
      //   let res = await this.deleteJob(id);
      //   if (res.status === 204) {
      //     this.$message.success("Занятие успешно удалено из шаблона");
      //     await this.fetchJobs();
      //   } else {
      //     this.$message.error("Произошла ошибка");
      //   }
      // } catch (e) {
      //   this.$message.error("Произошла ошибка");
      // } finally {
      //   this.loading = false;
      // }
    },

    async setForTheWeek(){

    },
    thisDateJobs(currDateString) {
      return this.jobs.filter((job)=>{
        return job.date == currDateString;
      })
    }
  },
  computed: {
    ...mapGetters({
      specialists: "specialists/getSpecialists",
      specialistsFetched: "activities/getFetched",
      activities: "activities/getActivities",
      activitiesFetched: "activities/getFetched",
    }),

    momentDateArr(){
      let momentFrom = moment(this.dateFrom).clone().weekday(0);
      let currMoment = momentFrom.clone();
      let momentTo = currMoment.clone().weekday(6);

      let dateArray = [];
      while (currMoment <= momentTo) {
          dateArray.push(currMoment.clone())
          currMoment = currMoment.add(1, 'days');
      }
      return dateArray;
    },
    dateIntervalString(){
      let momentFrom = this.momentDateArr[0];
      let momentTo = this.momentDateArr[this.momentDateArr.length-1];
      return `${momentFrom.format("D MMMM")} - ${momentTo.format("D MMMM")}`;
    },
  },
};
</script>

<style lang="sass">
.job-schedule
  display: flex
  flex-direction: column
  overflow: hidden
  height: 100%
  &__header
    display: flex
    flex-direction: column
    &-title
      flex-grow: 1
      text-align: center
      font-size: 1rem
      margin-bottom: 10px
    &__options
      display: flex
      flex-direction: row
      align-items: center
      justify-content: space-between
      margin-bottom: 10px
      &-navigate
        font-size: 20px
        display: flex
        flex-direction: row
        align-items: center
        justify-content: center
        &-to_left
          margin-right: 10px
        &-interval
          min-width: 250px
          text-align: center
        &-to_right
          margin-left: 10px
      &-button
  &__calendar
    overflow: auto
    flex: 1

    &__week
      display: flex
      flex-direction: row
      min-height: 100%

    &__date
      flex: 1 1 auto
      border-right: 1px solid #D9D9D9
      border-bottom: 1px solid #D9D9D9
      min-width: 150px
      max-width: 250px

      &:first-child
        border-left: 1px solid #D9D9D9

      &-title
        text-align: center
        border-bottom: 1px solid #D9D9D9
        background-color: #1890ff
        color: #FFFFFF
        font-size: 1rem
        position: sticky
        top: 0
        z-index: 2
        display: flex
        flex-direction: row
        align-items: center
        &-day
          margin: 4px 10px 4px 30px
          font-size: 18px
        &-weekday
          font-size: 34px
          font-weight: bold
          text-align: center
          flex: 1

    &__jobs
      padding: 15px 10px 10px 5px
</style>
