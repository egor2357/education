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
          <div class="job-schedule__calendar__date" v-for="item, index in 7" :key="index">
            <div class="job-schedule__calendar__date-title">
              {{ daysOfWeek[index].long }}
            </div>
            <div class="job-schedule__calendar__job">
              <a-timeline>
                <template v-for="job in jobs">
                  <a-timeline-item
                    v-if="index === job.day"
                    :color="job.activity.color"
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
                        <a-icon class="icon-button" type="dash"></a-icon>
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
      <job-modal
        v-if="displayModal"
        :activities="activities"
        :specialists="specialists"
        :editableData="modalEditableData"
        @closeModal="closeModal"
      />
    </div>
  </a-spin>
</template>

<script>
import JobModal from "@/components/JobSchedule/JobModal";
import { mapActions, mapGetters } from "vuex";
import consts from "@/const";
import datetime from "@/mixins/datetime";
import moment from "moment";

export default {
  components: {
    JobModal,
  },
  mixins: [
    datetime
  ],
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
    closeModal(){
      this.displayModal = false;
    },

    async fetchJobs(){

    },

    switchDates(isForward){
      let newMomentFrom = moment(this.dateFrom);
      if (isForward) {
        newMomentFrom = newMomentFrom.add(7, 'days');
      } else {
        newMomentFrom = newMomentFrom.subtract(7, 'days');
      }
      this.dateFrom = newMomentFrom.toDate();
    },

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
        this.loading = true;
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
        this.loading = false;
      }
    },

    async setForTheWeek(){

    },
  },
  computed: {
    ...mapGetters({
      specialists: "specialists/getSpecialists",
      specialistsFetched: "activities/getFetched",
      activities: "activities/getActivities",
      activitiesFetched: "activities/getFetched",
    }),

    dateArr(){
      let momentFrom = moment(this.dateFrom).clone().weekday(0);
      let currMoment = momentFrom.clone();
      let momentTo = currMoment.clone().weekday(6);

      let dateArray = [];
      while (currMoment <= momentTo) {
          dateArray.push( currMoment.toDate() )
          currMoment = currMoment.add(1, 'days');
      }
      return dateArray;
    },
    dateIntervalString(){
      let momentFrom = moment(this.dateArr[0]);
      let momentTo = moment(this.dateArr[this.dateArr.length-1]);
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
        padding: 10px
        color: #FFFFFF
        font-size: 1rem
        position: sticky
        top: 0
        z-index: 2

    &__job
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

          svg
            transform: rotate(90deg)
            margin-top: 3px

        &:hover
          .dropdown--hover
            display: unset

        .job-name
          flex: 0 0 100%
</style>
