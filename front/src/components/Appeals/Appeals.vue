<template>
  <a-spin :spinning="loading">
    <div class="appeals-block">
      <div class="top-bar">
        <div class="top-bar__side-block left"></div>
        <div class="title">Обращения к руководству</div>
        <div class="top-bar__side-block right">
          <a-button icon="plus" @click="displayAdd"> Добавить </a-button>
        </div>
      </div>
      <AppealsTable
        @startLoading="loading = true"
        @loaded="loading = false"
        @displayEdit="displayEdit"
        ref="appeals-table"
      />
      <AppealsModal
        v-if="displayModal"
        :adding="modalAdding"
        :editableData="modalEditableData"
        @closeSuccess="closeModalSuccess($event)"
        @close="displayModal = false"
      />
    </div>
  </a-spin>
</template>

<script>
import AppealsTable from "@/components/Appeals/AppealsTable";
import AppealsModal from "@/components/Appeals/AppealsModal";
import { mapActions, mapGetters } from "vuex";
export default {
  name: "Appeals",
  components: {
    AppealsTable,
    AppealsModal,
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
  },
  methods: {
    ...mapActions({
      fetchAppeals: "appeals/fetchAppeals",
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
    async closeModalSuccess(newAppealData) {
      this.displayModal = false;
      this.$router.push({
        name: "AppealDetails",
        params: { id: newAppealData.id, theme: newAppealData.theme }},
      );
    },
  },
};
</script>

<style lang="sass">
.appeals-block
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
    padding: 0 10%

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
</style>
