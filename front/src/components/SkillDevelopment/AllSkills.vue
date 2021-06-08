<template>
  <a-spin :spinning="loading">
    <div class="skill-development">
      <div class="skill-development__header">

        <div class="skill-development__header-title">
          Развитие навыков
        </div>

        <div class="skill-development__header__options">
          <div></div>
          <div class="skill-development__header__date-range">
            <span class="skill-development__header__date-range__label">Период:</span>
            <a-range-picker
              class="skill-development__header__date-range__input"
              v-model="dateRange"
              @change="dateRangeChange"
              format="DD.MM.YYYY"
              :allowClear="false"
              separator="-"/>
          </div>
        </div>

      </div>

      <div class="skill-development__body">
        <div class="skill-development__body__table">
          <div class="skill-development__body__table-header">
            <div class="skill-development__body__table-area">Образовательная область</div>
            <div class="skill-development__body__table-direction">Направление развития</div>
            <div class="skill-development__body__table-skill">Навык</div>
            <div class="skill-development__body__table-count">Количество обращений к навыку за период</div>
          </div>
          <div class="skill-development__body__table-body">

            <div class="skill-development__body__table-areas">
            <div class="skill-development__body__table-area-row"
              v-for="area in areas" :key="area.id">


              <div class="skill-development__body__table-area">
                {{ area.number }}. {{ area.name }}
              </div>

              <div class="skill-development__body__table-directions"
                v-if="area.development_directions.length">
              <div class="skill-development__body__table-direction-row"
                v-for="direction in area.development_directions" :key="direction.id">

                <div class="skill-development__body__table-direction">
                  {{ area.number }}.{{ direction.number }}. {{ direction.name }}
                </div>

                <div class="skill-development__body__table-skills"
                  v-if="direction.skills.length">
                <div class="skill-development__body__table-skill-row"
                  v-for="skill in direction.skills" :key="skill.id">

                  <div class="skill-development__body__table-skill skill-header"
                    @click="goToSkill(skill.id)">
                    {{ area.number }}.{{ direction.number }}.{{ skill.number }}. {{ skill.name }}
                  </div>
                  <div class="skill-development__body__table-count">
                    Количество
                  </div>

                </div>
                </div>

              </div>
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
import { mapActions, mapGetters } from "vuex";
// import consts from "@/const";
import moment from "moment";
// import deleteAxios from "@/middleware/deleteAxios";
// import post from "@/middleware/post";

export default {
  components: {
  },
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
  name: "AllSkills",
  data() {
    return {
      loading: true,

      dateRange: this.dateRangeInit,
    };
  },
  async created() {
    let fetches = []

    if (!this.areasFetched) {
      fetches.push(this.fetchAreas());
    }

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;

  },
  methods: {
    ...mapActions({
      fetchAreas: "skills/fetchAreas",
    }),

    // async fetchJobs(){
    //   try {
    //     this.loading = true;
    //     let firstQParameter = `date__gte=${this.momentDateArr[0].format("YYYY-MM-DD")}`;
    //     let secondQParameter = `date__lte=${this.momentDateArr[this.momentDateArr.length-1].format("YYYY-MM-DD")}`;
    //     let res = await this.$axios.get(`/api/jobs/?${firstQParameter}&${secondQParameter}`);
    //     if (res.status === 200) {
    //       this.jobs = res.data;
    //     } else {
    //       this.$message.error("Произошла ошибка при загрузке занятий");
    //     }
    //   } catch (e) {
    //     this.$message.error("Произошла ошибка при загрузке занятий");
    //   } finally {
    //     this.loading = false;
    //   }
    // },
    goToSkill(skillId){
      this.$router.push({name: "SkillDetails", params: {id: skillId}})
    },
    dateRangeChange(value){
      this.$emit("changeRange", value);
    },
  },
  computed: {
    ...mapGetters({
      areasFetched: "skills/getFetched",
      areas: "skills/getAreas",
    }),
  },

};
</script>

<style lang="sass">
.skill-development
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
    &__date-range
      display: flex
      flex-direction: row
      align-items: center
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

      &-body
        display: flex
        flex: 1
        flex-direction: column

      &-areas, &-directions, &-skills
        display: flex
        flex: 1
        flex-direction: column
      &-area-row, &-direction-row, &-skill-row
        display: flex
        flex: 1
        flex-direction: row
      &-area, &-direction, &-count
        min-width: 200px
        width: 200px
        padding: 10px 15px
        border-right: 1px solid #ccc
        border-bottom: 1px solid #ccc
      &-skill
        min-width: 200px
        flex: 1
        padding: 10px 15px
        border-right: 1px solid #ccc
        border-bottom: 1px solid #ccc
        &.skill-header
          color: #1890ff
          transition: all .3s cubic-bezier(.645,.045,.355,1)
          cursor: pointer
          &:hover
            color: #40a9ff



</style>
