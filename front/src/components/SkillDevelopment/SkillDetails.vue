<template>
  <a-spin :spinning="loading">
    <div class="skill-details">
      <div class="skill-details__header">

        <div class="skill-details__header-title">
          Развитие навыка
        </div>

        <div class="skill-details__header__options">
          <div class="skill-details__header__options__back">
            <a-button icon="left" @click="goBack">Назад</a-button>
          </div>
          <div class="skill-details__header__options__title"
            v-if="skillReports.length">
            {{ skillReports[0].skill.name }}
          </div>
          <div class="skill-details__header__options__date-range">
            <span class="skill-details__header__options__date-range__label">Период:</span>
            <a-range-picker
              class="skill-details__header__options__date-range__input"
              v-model="dateRange"
              @change="dateRangeChange"
              format="DD.MM.YYYY"
              :allowClear="false"
              separator="-"/>
          </div>
        </div>

      </div>

      <div class="skill-details__body">
        <div class="skill-details__body__table">
          <div class="skill-details__body__table-header">
            <div class="skill-details__body__table-date">Дата занятия</div>
            <div class="skill-details__body__table-activity">Вид деятельности</div>
            <div class="skill-details__body__table-specialist">Специалист</div>
            <div class="skill-details__body__table-job">Занятие</div>
          </div>
          <div class="skill-details__body__table-body">
            <div class="skill-details__body__table-row"
              v-for="skillReport in skillReports" :key="skillReport.id"
              @click="goToJob(skillReport.job)">
              <div class="skill-details__body__table-date">
                {{ skillReport.job.date | toRuDateString }}
              </div>
              <div class="skill-details__body__table-activity">
                <div :style="{
                  'background-color': `${skillReport.job.activity.color}10`,
                  border: `1px solid ${skillReport.job.activity.color}99`,
                }">
                  {{ skillReport.job.activity.name }}
                </div>
              </div>
              <div class="skill-details__body__table-specialist">
                {{ skillReport.job.specialist ? skillReport.job.specialist.__str__ : ""}}
              </div>
              <div class="skill-details__body__table-job">
                <div class="skill-details__body__table-job__text">
                  <div class="skill-details__body__table-job__topic">{{ skillReport.job.topic }}</div>
                  <div class="skill-details__body__table-job__form"
                    v-if="skillReport.job.method">
                    {{ skillReport.job.method.form_name }}
                  </div>
                  <div class="skill-details__body__table-job__method"
                    v-if="skillReport.job.method">
                    {{ skillReport.job.method.name }}
                  </div>
                </div>
                <div class="skill-details__body__table-job__mark"
                  :style="{'background-color': getColorByMark(skillReport.mark)}">
                </div>

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </a-spin>
</template>

<script>
import moment from "moment";
import getColorByMark from "@/mixins/getColorByMark"

export default {
  name: "SkillDetails",
  mixins: [getColorByMark],
  props: {
    dateRangeInit: {
      type: Array,
      default(){
        return [
          moment(new Date()).weekday(0),
          moment(new Date()).weekday(6)
        ];
      }
    },
  },
  data() {
    return {
      loading: true,

      dateRange: this.dateRangeInit,

      skillReports: [],
    };
  },
  computed: {

  },
  filters: {
    toRuDateString(value){
      return moment(value).format("DD.MM.YYYY");
    }
  },
  methods: {
    goBack(){
      this.$router.push({name: "AllSkills"});
    },
    dateRangeChange(value){
      this.$emit("changeRange", value);
    },
    async fetchSkillReports(){
      try {
        this.loading = true;
        let firstQParameter = `date_from=${this.dateRange[0].format("YYYY-MM-DD")}`;
        let secondQParameter = `date__to=${this.dateRange[1].format("YYYY-MM-DD")}`;
        let thirdQParameter = `is_affected=true`;
        let fourthQParameter = `skill_id=${this.$route.params.id}`;
        let QParameters = `?${firstQParameter}&${secondQParameter}&${thirdQParameter}&${fourthQParameter}`;
        let res = await this.$axios.get(`/api/skill_reports/${QParameters}`);
        if (res.status === 200) {
          this.skillReports = res.data;
        } else {
          this.$message.error("Произошла ошибка при загрузке отчетов");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка при загрузке отчетов");
      } finally {
        this.loading = false;
      }
    },
    goToJob(job) {
      if (job){
        this.$router.push({name: "JobDetails", params: {id: job.id}});
      }
    }
  },
  async created() {
    let fetches = []

    fetches.push(this.fetchSkillReports());

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;
  },
  beforeDestroy() {

  }
};
</script>

<style lang="sass">
.skill-details
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
      &__back
        display: flex
        flex-direction: row
        justify-content: flex-start
        flex: 1
      &__title
        display: flex
        flex-direction: row
        justify-content: center
        flex: 1
        font-size: 20px
      &__date-range
        display: flex
        flex-direction: row
        flex: 1
        align-items: center
        justify-content: flex-end
        &__label
          margin-right: 10px

  &__body
    &__table
      display: flex
      flex: 1
      flex-direction: column
      border-left: 1px solid #ccc
      border-top: 1px solid #ccc
      &-header
        display: flex
        flex: 1
        flex-direction: row
        background-color: #f4f4f4
        color: rgba(0, 0, 0, 0.85)
        div
          display: flex
          align-items: center
      &-body
        display: flex
        flex: 1
        flex-direction: column
      &-row
        display: flex
        flex: 1
        flex-direction: row
        background: white
        transition: background 0.3s
        &:hover
          background: #e6f7ff
          cursor: pointer
      &-date, &-specialist
        min-width: 200px
        width: 200px
        padding: 10px 15px
        border-right: 1px solid #ccc
        border-bottom: 1px solid #ccc
      &-activity
        min-width: 200px
        width: 200px
        padding: 10px 15px
        border-right: 1px solid #ccc
        border-bottom: 1px solid #ccc
        div
          padding: 2px 4px
          text-align: center
          border-radius: 4px
      &-job
        display: flex
        flex-direction: row
        flex: 1
        min-width: 200px
        padding: 10px 15px
        border-right: 1px solid #ccc
        border-bottom: 1px solid #ccc
        &__text
          display: flex
          flex-direction: row
          flex: 1
        &__mark
          height: 26px
          width: 26px
          border-radius: 13px
          box-shadow: 0 1px 3px 1px #dedede
        &__topic
          margin-right: 10px
          font-weight: bold
        &__form
          margin-right: 10px


</style>
