<template>
  <a-spin :spinning="loading">
    <div class="missions-block">
      <div class="top-bar">
        <div class="top-bar__side-block left"></div>
        <div class="title">Задачи</div>
        <div class="top-bar__side-block right">
          <a-button icon="plus" v-if="isStaff" @click="displayAdd">
            Добавить задачу
          </a-button>
        </div>
      </div>
      <MissionsTable
        @startLoading="loading = true"
        @loaded="loading = false"
        @displayEdit="displayEdit"
        ref="mission-table"
      />
      <MissionsModal
        v-if="displayModal"
        :adding="modalAdding"
        :editableData="modalEditableData"
        @closeSuccess="closeModalSuccess"
        @close="displayModal = false"
      />
    </div>
  </a-spin>
</template>

<script>
import MissionsTable from "@/components/Missions/MissionsTable";
import MissionsModal from "@/components/Missions/MissionsModal";
import { mapActions, mapGetters } from "vuex";
export default {
  name: "Missions",
  components: {
    MissionsTable,
    MissionsModal,
  },
  data() {
    return {
      loading: true,
      displayModal: false,
      modalAdding: true,
      modalEditableData: null,
    };
  },
  async created() {
    if (!this.specialistsFetched) {
      await this.fetchSpecialists();
    }
  },
  computed: {
    ...mapGetters({
      specialistsFetched: "specialists/getFetched",
    }),
    isStaff() {
      return this.$store.getters["auth/getUserInfo"].staff;
    },
  },
  methods: {
    ...mapActions({
      fetchMissions: "missions/fetchMissions",
      fetchSpecialists: "specialists/fetchSpecialists",
    }),
    displayAdd() {
      this.displayModal = true;
      this.modalAdding = true;
    },
    displayEdit(data) {
      this.displayModal = true;
      this.modalAdding = false;
      this.modalEditableData = data;
    },
    async closeModalSuccess() {
      this.displayModal = false;
      await this.fetchMissions();
      this.$refs['mission-table'].updatePaginationTotal();
    },
  },
};
</script>

<style lang="sass">
.missions-block
  display: flex
  flex-direction: column
  overflow: hidden
  height: 100%

  .top-bar
    display: flex
    margin-bottom: 10px
    line-height: 32px

    .title
      font-size: 1rem
      text-align: center
      margin: 0 10px

  .top-bar__side-block
    flex: 1

    &.right
      text-align: right

  .ant-table-wrapper
    flex: 1 1 auto
    overflow: auto

    .ant-spin-container
      display: flex
      flex-direction: column

      .ant-table
        overflow: hidden

        .ant-table-content
          overflow: auto
          height: 100%

      .ant-table-pagination
        text-align: right

    table
      border-top: 0

    .ant-table-thead
      th
        position: sticky
        position: -webkit-sticky
        top: 0
        border-top: 1px solid #e8e8e8

.ant-modal-missions
  .ant-modal-body
    max-height: 550px
</style>
