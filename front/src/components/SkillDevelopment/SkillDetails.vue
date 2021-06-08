<template>
  <a-spin :spinning="loading">
    <div class="skill-details">
      <div class="skill-details__header">

        <div class="skill-details__header-title">
          Развитие навыка
        </div>

        <div class="skill-details__header__options">
          <a-button
            icon="left" @click="goBack">Назад</a-button>
          <div></div>
          <div class="skill-details__header__date-range">
            <span class="skill-details__header__date-range__label">Период:</span>
            <a-range-picker
              class="skill-details__header__date-range__input"
              v-model="dateRange"
              @change="dateRangeChange"
              format="DD.MM.YYYY"
              :allowClear="false"
              separator="-"/>
          </div>
        </div>

      </div>

      <div class="skill-details__body">

      </div>
    </div>
  </a-spin>
</template>

<script>
import moment from "moment";

export default {
  name: "SkillDetails",
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
  methods: {
    goBack(){
      this.$router.go(-1);
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
</style>
