<template>
  <a-spin :spinning="loading">
    <div class="job-details">
      <div class="job-details__header">

        <div class="job-details__header-title" v-if="job">
          <div class="job-details__header-title__activity">
            <div :style="{
              'background-color': `${job.activity.color}10`,
              border: `1px solid ${job.activity.color}99`,
            }">
              {{ job.activity.name }}
            </div>
          </div>
          <div class="job-details__header-title__date">
            <div class="job-details__header-title__date-day">
              {{ job.dateMoment.format("D MMMM") }}
            </div>
            <div class="job-details__header-title__date-weekday">
              {{ job.dateMoment.format("dddd") }}
            </div>
          </div>
          <div class="job-details__header-title__specialist">
            <div class="job-details__header-title__specialist-label">Специалист:</div>
            <div class="job-details__header-title__specialist-name">{{ job.specialist.__str__ }}</div>
          </div>
        </div>

        <div class="job-details__header__options">
          <div class="job-details__header__options__back">
            <a-button icon="left" @click="goBack">Назад</a-button>
          </div>
          <a-radio-group v-model="isJobWindow">
            <a-radio-button :value="true">Параметры занятия</a-radio-button>
            <a-radio-button :value="false">Отчет</a-radio-button>
          </a-radio-group>
        </div>

      </div>

      <div class="job-details__body" v-if="job">

        <a-form-model :model="job" v-bind="layout" :rules="rules" ref="jobForm">

          <a-form-model-item prop="topic" label="Тема занятия" key="topic"
            :validateStatus="fields['topic'].validateStatus" :help="fields['topic'].help">
            <a-input v-model="job.topic" />
          </a-form-model-item>

          <a-form-model-item prop="reports" label="Навыки" key="reports"
            :validateStatus="fields['reports'].validateStatus" :help="fields['reports'].help">
            <a-tree-select
              v-model="job.skills"
              placeholder="Выберите навыки"
              allow-clear multiple
              >
              <a-tree-select-node v-for="area in areas"
                :key="'area'+area.id"
                :value="'area'+area.id"
                :selectable="false"
                :title="area.name">
                <a-tree-select-node v-for="direction in area.development_directions"
                  :key="'direction'+direction.id"
                  :value="'direction'+direction.id"
                  :selectable="false"
                  :title="direction.name">
                  <a-tree-select-node v-for="skill in direction.skills"
                    :key="'skill'+skill.id"
                    :value="skill.id"
                    :title="skill.name"
                    :isLeaf="true">
                  </a-tree-select-node>
                </a-tree-select-node>
              </a-tree-select-node>
            </a-tree-select>
          </a-form-model-item>

        </a-form-model>

      </div>
    </div>
  </a-spin>
</template>

<script>
import moment from "moment";
import getColorByMark from "@/mixins/getColorByMark"
import { mapActions, mapGetters } from "vuex";

export default {
  name: "JobDetails",
  mixins: [getColorByMark],
  props: {
  },
  data() {
    return {
      loading: true,

      job: null,

      isJobWindow: true,
      layout: {
        labelCol: { span: 6 },
        wrapperCol: { span: 14 },
      },

      fields: {
        'topic': {
          validateStatus: "",
          help: "",
        },
        'reports': {
          validateStatus: "",
          help: "",
        },
      },
      rules: {
        topic: [
          {
            trigger: "change",
            required: true,
            message: "Пожалуйста, введите название темы",
          },
        ],
        reports: [
          {
            trigger: "change",
            required: false,
            message: "Пожалуйста, выберите затрагиваемые навыки",
          },
        ],
      },
    };
  },
  computed: {
    ...mapGetters({
      areasFetched: "skills/getFetched",
      areas: "skills/getAreas",
    }),
  },
  methods: {
    ...mapActions({
      fetchAreas: "skills/fetchAreas",
    }),

    goBack(){
      this.$router.go(-1);
    },
    async fetchJob(){
      try {
        this.loading = true;
        let jobId = this.$route.params.id;
        let res = await this.$axios.get(`/api/jobs/${jobId}`);
        if (res.status === 200) {
          this.job = res.data;
          this.job.dateMoment = moment(this.job.date, "YYYY-MM-DD");
          this.job.skills = this.job.reports.map((report)=>{
            return report.skill_id;
          });
        } else {
          this.$message.error("Произошла ошибка при загрузке занятия");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка при загрузке занятия");
      } finally {
        this.loading = false;
      }
    },
  },
  async created() {
    let fetches = []

    if (!this.areasFetched) {
      fetches.push(this.fetchAreas());
    }

    fetches.push(this.fetchJob());

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;
  },
  beforeDestroy() {

  }
};
</script>

<style lang="sass">
.job-details
  display: flex
  flex-direction: column
  overflow: hidden
  height: 100%
  &__header
    display: flex
    flex-direction: column
    &-title
      display: flex
      flex-direction: row
      justify-content: center
      align-items: center
      flex: 1
      text-align: center
      font-size: 1rem
      margin-bottom: 10px
      &__activity
        display: flex
        margin-right: 20px
        max-width: 400px
        div
          padding: 2px 4px
          text-align: center
          border-radius: 4px
      &__date
        display: flex
        flex-direction: column
        align-items: center
        margin-right: 20px
        &-day
          color: rgba(0, 0, 0, 0.85)
          font-size: 20px
          line-height: 22px
          &:first-letter
            font-weight: bold
        &-weekday
          font-size: 18px
          line-height: 20px
      &__specialist
        display: flex
        flex-direction: row
        &-label
          margin-right: 10px
        &-name
          color: rgba(0, 0, 0, 0.85)


    &__options
      display: flex
      flex-direction: row
      align-items: center
      justify-content: space-between
      margin-bottom: 10px
      &__back
        display: flex
        flex-direction: row
        justify-content: flex-start

  &__body


</style>