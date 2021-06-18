<template>
  <a-spin :spinning="loading">
    <div class="job-options">
      <div class="job-options__header">
        <div class="job-options__header-filler"></div>
        <div>Планы занятий</div>
        <div class="job-options__header-filler">
          <a-button @click="showModal(null)" v-if="activities.length">
            <a-icon type="plus"/>Добавить план занятия
          </a-button>
        </div>
      </div>
      <div class="job-options__tabs" v-if="activities.length">
        <a-tabs v-model="activeTab">
          <a-tab-pane v-for="activity in activities" :key="activity.id">
            <span slot="tab">
              {{ activity.name }}
            </span>
          </a-tab-pane>
        </a-tabs>
      </div>
      <div class="job-options__cards" v-if="currentActivityOptions.length">
        <div class="job-options__card" v-for="option in currentActivityOptions" :key="option.id">
          <job-option :option="option">
            <div class="job-option-header-actions">
              <div class="job-option-header-action"
                @click="showModal(option)">
                Изменить
              </div>
              <a-divider type="vertical" />
              <div class="job-option-header-action"
                @click="deleteOption(option)">
                Удалить
              </div>
            </div>
          </job-option>
        </div>
      </div>
      <div v-else>
        <a-empty :image="simpleImage"/>
      </div>

    </div>
  </a-spin>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import JobOption from "@/components/JobOptions/JobOption";
import { Empty } from 'ant-design-vue';

export default {
  components: {
    JobOption
  },
  name: "JobOptions",
  data() {
    return {
      loading: true,

      activeTab: null,

      options: [],

      isModalVisible: false,

    };
  },
  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },
  async created() {
    let fetches = []

    if (!this.activitiesFetched) {
      fetches.push(this.fetchActivities());
    }

    fetches.push(this.fetchOptions());

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;

    if (this.activities.length) {
      this.activeTab = this.activities[0].id;
    }

  },
  methods: {
    async fetchOptions(){
      try {
        this.loading = true;
        let res = await this.$axios.get("/api/options");
        if (res.status === 200) {
          this.options = res.data;
        } else if (res.status === 400) {
          this.$message.error("Ошибка при загрузке планов занятий специалиста");
        } else {
          this.$message.error("Ошибка при загрузке планов занятий специалиста");
        }
      } catch (e) {
        this.$message.error("Ошибка при загрузке планов занятий специалиста");
      } finally {
        this.loading = false;
      }
    },


    showModal(){
      this.isModalVisible = true;
    },
    closeModal(){
      this.isModalVisible = false;
    },

    createOption(){

    },
    editOption(option){

    },
    deleteOption(option){

    },

    ...mapActions({
      fetchActivities: "activities/fetchActivities",
    }),
  },
  computed: {
    ...mapGetters({
      activitiesFetched: "activities/getFetched",
      activities: "activities/getActivities",
    }),

    currentActivityOptions(){
      return this.options.filter((option)=>{
        return option.activity_id == this.activeTab;
      })
    }
  },
};
</script>

<style lang="sass">
  .job-options
    display: flex
    flex-direction: column
    height: 100%
    overflow: hidden
    &__header
      display: flex
      flex-direction: row
      align-items: center
      margin-bottom: 10px
      font-size: 16px
      &-filler
        flex: 1
        text-align: right
    &__tabs
      display: flex
      justify-content: center
    &__cards
      display: flex
      flex-direction: column
      flex: 1
      overflow-y: auto
      margin-top: 10px
      width: 900px
      margin: 10px auto 0

    &__card
      position: relative
</style>
