<template>
  <a-spin :spinning="loading">
    <div class="job-schedule">
      <div class="job-schedule-label">
        <span class="title">Расписание занятий</span>
        <span>
          <a-button icon="plus" @click="openModal(null)">
            Добавить занятие
          </a-button>
        </span>
      </div>
      <job-calendar
        :jobs="jobs"
        @openModal="openModal($event)"/>
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
import JobCalendar from "@/components/JobSchedule/JobCalendar";
import { mapActions, mapGetters } from "vuex";

export default {
  components: {
    JobCalendar,
    JobModal,
  },
  name: "JobSchedule",
  data() {
    return {
      loading: true,
      displayModal: false,
      modalEditableData: null,

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
  },
  computed: {
    ...mapGetters({
      specialists: "specialists/getSpecialists",
      specialistsFetched: "activities/getFetched",
      activities: "activities/getActivities",
      activitiesFetched: "activities/getFetched",
    }),
  },
};
</script>

<style lang="sass">
.job-schedule
  display: flex
  flex-direction: column
  overflow: hidden
  height: 100%
  .job-schedule-label
    display: flex
    margin-bottom: 10px
    .title
      flex-grow: 1
      text-align: center
      font-size: 1rem
</style>
