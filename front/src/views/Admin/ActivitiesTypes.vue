<template>
  <div class="activities-container">
    <div class="top-bar">
      <div class="top-bar__side-block left"></div>
      <div class="title">Виды деятельности</div>
      <div class="top-bar__side-block right">
        <a-button v-if="activeTab == 1" icon="plus" type="secondary" @click="onAddActivity">Добавить</a-button>
      </div>
    </div>
    <a-tabs v-model="activeTab" class="tabs--center">
      <a-tab-pane key="1">
        <span slot="tab">
          <a-icon type="unordered-list" />
          Список
        </span>
      </a-tab-pane>
      <a-tab-pane key="2">
        <span slot="tab">
          <a-icon type="share-alt" />
          Вид деятельности / навыки
        </span>
      </a-tab-pane>
    </a-tabs>
    <div class="tab-content">
      <TypesList
        v-if="activeTab == 1"
        :data="activities"
        @needUpdate="fetchActivities"
        :loadingList="loadingList"
        @onEditActivity="onEditActivity"
        @onDeleteActivity="onDeleteActivity"
      />
      <ActivitiesSkills
        v-if="activeTab == 2"
      />
    </div>
    <ModalActivities
      v-if="displayModal"
      :adding="modalAdding"
      :editableData="modalEditableData"
      @close="displayModal = false"
      @closeSuccess="
        displayModal = false;
        fetchActivities()
      "
    />
  </div>
</template>

<script>
import TypesList from "@/components/ActivitiesTypes/TypesList";
import ActivitiesSkills from "@/components/ActivitiesTypes/ActivitiesSkills";
import ModalActivities from "@/components/ActivitiesTypes/ModalActivities";
import { mapActions, mapGetters } from "vuex";
export default {
  name: "ActivitiesTypes",
  components: {
    TypesList,
    ActivitiesSkills,
    ModalActivities
  },
  data() {
    return {
      activeTab: "1",
      loadingList: true,
      displayModal: false,
      modalAdding: true,
      modalEditableData: null,
    };
  },
  async created() {
    await this.fetchActivities();
    this.loadingList = false;
  },
  methods: {
    ...mapActions({
      fetchActivities: "activities/fetchActivities",
    }),
    onAddActivity(){
      this.displayModal = true;
      this.modalEditableData = {};
      this.modalAdding = true;
    },
    onEditActivity(activity){
      this.displayModal = true;
      this.modalEditableData = activity;
      this.modalAdding = false;
    },
    onDeleteActivity(activity){
      let that = this;
      this.$confirm({
        title: `Вы действительно хотите удалить вид деятельности ${activity.name}?`,
        content: ``,
        okType: "danger",
        onOk() {
          that.deleteRecord(activity.id);
        },
      });
    },
    async deleteRecord(id) {
      this.loading = true;
      try {
        let res = await this.$store.dispatch("activities/deleteActivity", id);
        if (res.status === 204) {
          this.$message.success("Вид деятельности успешно удалён");
          await this.fetchActivities();
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      } finally {
        this.loading = false;
      }
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
.activities-container
  height: 100%
  display: flex
  flex-direction: column

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

  .tabs--center
    margin: 0 auto

  .tab-content
    flex: 1
    overflow: hidden

</style>
