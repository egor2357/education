<template>
  <a-spin :spinning="loading">
    <div class="task-groups-block">
      <div class="top-bar">
        <div class="top-bar__side-block left">
          <a-radio-group v-model="questionsSelected" @change="changeRoute">
            <a-radio-button :value="false">
              Благодарности и успехи
            </a-radio-button>
            <a-radio-button :value="true"> Открытые вопросы </a-radio-button>
          </a-radio-group>
        </div>
        <div class="title">Интервенционные группы</div>
        <div class="top-bar__side-block right">
          <a-button icon="plus" @click="displayAdd"> Добавить </a-button>
        </div>
      </div>
      <TaskGroupsTable
        @startLoading="loading = true"
        @loaded="loading = false"
        @displayEdit="displayEdit"
        ref="task-groups-table"
        :questionsSelected="questionsSelected"
      />
      <TaskGroupsModal
        v-if="displayModal"
        :adding="modalAdding"
        :editableData="modalEditableData"
        @closeSuccess="closeModalSuccess"
        @close="displayModal = false"
        :questionsSelected="questionsSelected"
      />
    </div>
  </a-spin>
</template>

<script>
import TaskGroupsTable from "@/components/TaskGroups/TaskGroupsTable";
import TaskGroupsModal from "@/components/TaskGroups/TaskGroupsModal";
import { mapActions, mapGetters } from "vuex";
export default {
  name: "TaskGroups",
  components: {
    TaskGroupsTable,
    TaskGroupsModal,
  },
  data() {
    return {
      loading: true,
      displayModal: false,
      modalAdding: true,
      modalEditableData: null,
      questionsSelected: false,
    };
  },
  async created() {
    if (this.$route.query["is_question"]) {
      this.$route.query["is_question"] === "false"
        ? (this.questionsSelected = false)
        : (this.questionsSelected = true);
    }
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
      fetchTaskGroups: "taskGroups/fetchTaskGroups",
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
      await this.fetchTaskGroups();
      this.$refs["task-groups-table"].updatePaginationTotal();
    },
    async changeRoute(event) {
      this.$set(this, "questionsSelected", event.target.value);
      this.$router.push({ query: { is_question: this.questionsSelected } });
      await this.$refs["task-groups-table"].getData(this.questionsSelected);
    },
  },
};
</script>

<style lang="sass">
.task-groups-block
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
</style>
