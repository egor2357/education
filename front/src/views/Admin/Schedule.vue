<template>
  <div style="height: 100%">
    <a-spin :spinning="loading">
      <div class="schedule-label">
        <span><a-button icon="bar-chart" @click="displayChart = true"></a-button></span>
        <span class="title">Шаблон расписания занятий</span>
        <span
          ><a-button
            icon="plus"
            @click="
              displayModal = true;
              modalAdding = true;
              modalEditableData = null;
            "
            >Добавить занятие</a-button
          ></span
        >
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
    </a-spin>
  </div>
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
    this.loading = true;
    await this.fetchActivities();
    this.loading = false;
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
    }),
  },
};
</script>

<style lang="sass">
.schedule-label
  display: flex
  margin-bottom: 10px
  .title
    flex-grow: 1
    text-align: center
    font-size: 1rem
</style>
