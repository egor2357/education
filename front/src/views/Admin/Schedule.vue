<template>
  <a-spin :spinning="loading">
    <div class="schedule">
      <div class="top-bar">
        <div class="top-bar__side-block left">
          <a-button icon="bar-chart" @click="displayChart = true">Статистика</a-button>
        </div>
        <span class="title">Шаблон расписания занятий</span>
        <div class="top-bar__side-block right">
          <a-button
            icon="plus"
            @click="
              displayModal = true;
              modalAdding = true;
              modalEditableData = null;
            "
            >Добавить занятие</a-button>
        </div>
      </div>
      <Template
        @startLoading="loading = true"
        @endLoading="loading = false"
        @displayModal="displayModal = true"
        @openModalEdit="openModalEdit"
      />
      <ModalTemplateJob
        v-if="displayModal"
        @close="displayModal = false"
        :activities="activities"
        :adding="modalAdding"
        :editableData="modalEditableData"
        @closeSuccess="
          displayModal = false;
          fetchJobs();
        "
      />
      <ModalChart v-if="displayChart" @close="displayChart = false"/>
    </div>
  </a-spin>
</template>

<script>
import ModalTemplateJob from "@/components/Schedule/ModalTemplateJob";
import Template from "@/components/Schedule/Template";
import ModalChart from "@/components/Schedule/ModalChart";
import { mapActions, mapGetters } from "vuex";
export default {
  components: {
    Template,
    ModalTemplateJob,
    ModalChart
  },
  name: "Schedule",
  data() {
    return {
      loading: true,
      displayModal: false,
      modalAdding: true,
      modalEditableData: null,
      displayChart: false,
    };
  },
  async created() {
    if (!this.activitiesFetched)
    {
      this.loading = true;
      await this.fetchActivities();
      this.loading = false;
    }
  },
  methods: {
    ...mapActions({
      fetchActivities: "activities/fetchActivities",
      fetchJobs: "schedule/fetchJobs",
    }),
    openModalEdit(job) {
      this.displayModal = true;
      this.modalAdding = false;
      this.modalEditableData = job;
    },
  },
  computed: {
    ...mapGetters({
      activities: "activities/getActivities",
      activitiesFetched: "activities/getFetched"
    }),
  },
};
</script>

<style lang="sass">
.schedule
  display: flex
  flex-direction: column
  overflow: hidden
  height: 100%
  .top-bar
    display: flex
    margin-bottom: 10px
    .top-bar__side-block
      flex: 1
      &.right
        text-align: right
    .title
      text-align: center
      font-size: 1rem
</style>
