<template>
  <a-spin :spinning="loading">
    <div class="skill-development">
      <div class="top-bar">
        <div class="top-bar__side-block left">
          <a-select
            :value="displayMode"
            @change="changeDisplayMode"
            style="width: 330px"
          >
            <a-select-option value="all">Все навыки и упражнения</a-select-option>
            <a-select-option value="called">Только затронутые навыки и упражнения</a-select-option>
            <a-select-option value="notCalled">Только не затронутые навыки и упражнения</a-select-option>
          </a-select>
        </div>
        <div class="title">Развитие навыков</div>
        <div class="top-bar__side-block right">
          <span class="date-range-label">Период:</span>
          <a-range-picker
            class="date-range-input"
            :value="dateRange"
            @change="dateRangeChange"
            format="DD.MM.YYYY"
            :allowClear="false"
            separator="-"
          />
        </div>
      </div>

      <div id="table" class="skill-table">
        <div>
          <div v-if="filteredAreas.length" class="skill-table__body">
            <div v-for="area in filteredAreas" :key="area.id">
              <div
                class="skill-table__cell skill-table__cell_sticky skill-table-area"
              >
                <a-icon
                  class="icon-button icon-show"
                  :class="{'icon-show-hidden': !area.development_directions.length}"
                  :type="shownAreas.includes(area.id) ? 'down' : 'right'"
                  @click="toggleArea(area.id)"
                />
                <span
                  >
                  {{ [area.number, area.name].join(". ") }}</span
                >
              </div>
              <Transition name="show">
                <div v-if="shownAreas.includes(area.id)" class="skill-table-direction-wrapper">
                  <div
                    v-for="direction in area.development_directions"
                    :key="direction.id"
                  >
                    <div
                      class="skill-table__cell skill-table__cell_sticky skill-table-direction"
                    >
                      <a-icon
                        class="icon-button icon-show"
                        :class="{'icon-show-hidden': !direction.skills.length}"
                        :type="shownDirections.includes(direction.id) ? 'down' : 'right'"
                        @click="toggleDirection(direction.id)"
                      />
                      <span>
                        {{
                          [area.number, direction.number].join(".") +
                            ". " +
                            direction.name
                        }}
                      </span>
                    </div>
                    <Transition name="show">
                      <div v-if="shownDirections.includes(direction.id)">
                        <div v-for="skill in direction.skills" :key="skill.id">
                          <div
                            class="skill-table__skill-cell skill-table__cell_sticky"
                          >
                            <div class="skill-table__skill__name">
                              <a-icon
                                class="icon-button icon-show"
                                :class="{'icon-show-hidden': !skill.exercises.length}"
                                :type="shownSkills.includes(skill.id)  ? 'down' : 'right'"
                                @click="toggleSkill(skill.id)"
                              />
                              <span>
                                {{ [ area.number, direction.number, skill.number].join(".") +
                                    ". " + skill.name }}
                              </span>
                            </div>
                            <div class="skill-table__skill__calls">
                              <a-popover title="Выполнение плана" placement="left">
                                {{
                                  skill.id in skillsStatisticsById
                                    ? skillsStatisticsById[skill.id].called
                                    : 0
                                }}
                                /
                                {{
                                  skill.id in skillsStatisticsById
                                    ? skillsStatisticsById[skill.id].planned
                                    : 0
                                }}
                                <template #content>
                                  <b>Оцененные</b> упражнения <b>/</b> <b>Запланированные</b> упражнения
                                </template>
                              </a-popover>
                            </div>
                            <div class="skill-table__skill__mark">
                              <a-popover title="Уровень освоения" placement="left">
                                {{
                                  skill.id in skillsStatisticsById
                                    ? skillsStatisticsById[skill.id].value
                                    : "-"
                                }}
                                <template #content>
                                  Среднее значение уровня выполнения всех<br>
                                  <b>запланированных</b> занятий
                                </template>
                              </a-popover>
                            </div>
                          </div>
                          <Transition name="show">
                            <div
                              v-if="shownSkills.includes(skill.id)"
                              class="skill-table-exercises"
                            >
                              <div class="skill-table-exercises__content">
                                <div
                                  v-for="exercise in skill.exercises"
                                  :key="exercise.id"
                                  class="skill-table__exercise-cell"
                                >
                                  <div class="skill-table__exercise-cell__name">
                                    <span
                                      :class="{
                                        'exercise-link': reportsStatisticsById[exercise.id]
                                      }"
                                      @click="goToExercise(exercise.id)"
                                    >
                                      {{
                                        [ area.number, direction.number, skill.number, exercise.number].join(".") +
                                        '. ' + exercise.name
                                      }}
                                    </span>
                                  </div>
                                  <div class="skill-table__exercise-cell__calls">
                                    <a-popover title="Выполнение плана" placement="left">
                                      {{
                                        exercise.id in reportsStatisticsById
                                          ? reportsStatisticsById[exercise.id].called
                                          : 0
                                      }}
                                      /
                                      {{
                                        exercise.id in reportsStatisticsById
                                          ? reportsStatisticsById[exercise.id].planned
                                          : 0
                                      }}
                                      <template #content>
                                        <b>Оцененные</b> упражнения <b>/</b> <b>Запланированные</b> упражнения
                                      </template>
                                    </a-popover>
                                  </div>
                                  <div class="skill-table__exercise-cell__mark">
                                    <a-popover title="Уровень освоения" placement="left">
                                      {{
                                        exercise.id in reportsStatisticsById
                                          ? reportsStatisticsById[exercise.id].value
                                          : "-"
                                      }}
                                      <template #content>
                                        Среднее значение уровня выполнения всех<br>
                                        <b>запланированных</b> занятий
                                      </template>
                                    </a-popover>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </Transition>
                        </div>
                      </div>
                    </Transition>
                  </div>
                </div>
              </Transition>
            </div>
          </div>
          <div class="skill-table__no-data" v-else>
            <a-empty :image="simpleImage" />
          </div>
        </div>
      </div>

    </div>
  </a-spin>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from "vuex";
import { Empty } from "ant-design-vue";
import moment from "moment";

export default {
  components: {},
  props: {
    dateRangeInit: {
      type: Array,
      default() {
        return [moment(new Date()).weekday(0), moment(new Date()).weekday(6)];
      }
    }
  },
  name: "AllSkills",
  data() {
    return {
      loading: true,

      dateRange: [],
      displayMode: "all",

      reportsStatisticsById: {},
      skillsStatisticsById: {},

      shownAreas: [],
      shownDirections: [],
      shownSkills: [],
    };
  },

  computed: {

    ...mapGetters({
      areasFetched: "skills/getFetched",
      areas: "skills/getAreas",
      skillDevelopmentTreeState: "skills/getSkillDevelopmentTreeState"
    }),

    filteredAreas() {
      let checkFunction;
      if (this.displayMode == "called") {
        checkFunction = (exercise) => {
          return String(exercise.id) in this.reportsStatisticsById;
        }
      } else if (this.displayMode == "notCalled") {
        checkFunction = (exercise) => {
          return !(String(exercise.id) in this.reportsStatisticsById);
        }
      } else {
        checkFunction = (exercise) => {
          return true;
        }
      }

      return this.areas
        .map(area => {
          return {
            id: area.id,
            name: area.name,
            number: area.number,
            development_directions: area.development_directions
              .map(dir => {
                return {
                  id: dir.id,
                  area_id: dir.area_id,
                  name: dir.name,
                  number: dir.number,
                  skills: dir.skills
                    .map(skill => {
                      return {
                        id: skill.id,
                        direction_id: skill.direction_id,
                        name: skill.name,
                        number: skill.number,
                        exercises: skill.exercises.filter(checkFunction)
                      };
                    })
                    .filter(skill => skill.exercises.length)
                };
              })
              .filter(direction => direction.skills.length)
          };
        })
        .filter(area => area.development_directions.length);
    },
  },

  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },

  async created() {
    let fetches = [];

    if (!this.areasFetched) {
      fetches.push(this.fetchAreas());
    }

    if (this.$route.query.displayMode) {
      this.displayMode = this.$route.query.displayMode;
    }

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;

    if (!this.setDateRange(this.$route)) {
      this.dateRangeChange(this.dateRange, true);
      return;
    }

    await this.fetchSkillReportsStatistics();
    this.setupSkillDevelopmentTreeState();
  },

  async beforeRouteUpdate(to, from, next) {
    if (!this.setDateRange(to)) {
      this.dateRangeChange(this.dateRange, true);
      return;
    }

    if (from.name != 'ExerciseDetails') {
      this.clearSkillDevelopmentTreeState();
    }

    this.setupSkillDevelopmentTreeState();

    if (to.query.displayMode) {
      this.displayMode = to.query.displayMode;
    }

    await this.fetchSkillReportsStatistics();

    next();
  },

  async beforeRouteLeave(to, from, next) {
    // Для всех путей,кроме просмотра отчета по упражнению
    // Скидываем состояние дерева и скролла
    if (to.name == 'ExerciseDetails') {
      this.saveSkillDevelopmentTreeState();
    } else {
      this.clearSkillDevelopmentTreeState();
    }

    next();
  },


  methods: {

    ...mapActions({
      fetchAreas: "skills/fetchAreas"
    }),

    ...mapMutations({
      setSkillDevelopmentTreeState: "skills/setSkillDevelopmentTreeState"
    }),

    async fetchSkillReportsStatistics() {
      try {
        this.loading = true;
        let firstQParameter = `date_from=${this.dateRange[0].format(
          "YYYY-MM-DD"
        )}`;
        let secondQParameter = `date_to=${this.dateRange[1].format(
          "YYYY-MM-DD"
        )}`;
        let QParameters = `?${firstQParameter}&${secondQParameter}`;
        let res = await this.$axios.get(
          `/api/exercise_reports/statistics/${QParameters}`
        );
        if (res.status === 200) {
          this.reportsStatisticsById = res.data.reports;
          this.skillsStatisticsById = res.data.skills;
        } else {
          this.$message.error("Произошла ошибка при загрузке отчетов");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка при загрузке отчетов");
      } finally {
        this.loading = false;
      }
    },

    dateRangeChange(value, replace = false) {
      if (
        value[0].format("YYYY-MM-DD") == this.$route.query.dateFrom &&
        value[1].format("YYYY-MM-DD") == this.$route.query.dateTo
      ) {
        return;
      }

      let queryObj = {
        dateFrom: value[0].format("YYYY-MM-DD"),
        dateTo: value[1].format("YYYY-MM-DD"),
        displayMode: this.displayMode
      };

      if (replace) {
        this.$router
          .replace({
            name: this.$route.name,
            query: queryObj
          })
          .catch(() => {});
      } else {
        this.$router
          .push({
            name: this.$route.name,
            query: queryObj
          })
          .catch(() => {});
      }
    },

    setDateRange(route) {
      let query = route.query;
      if (
        !Object.prototype.hasOwnProperty.call(query, "dateFrom") ||
        !Object.prototype.hasOwnProperty.call(query, "dateTo")
      ) {
        this.dateRange.splice(0);
        this.dateRange.push(this.dateRangeInit[0].clone());
        this.dateRange.push(this.dateRangeInit[1].clone());
        return false;
      } else {
        this.dateRange.splice(0);
        this.dateRange.push(moment(query.dateFrom, "YYYY-MM-DD"));
        this.dateRange.push(moment(query.dateTo, "YYYY-MM-DD"));
        return true;
      }
    },

    changeDisplayMode(value) {
      this.$router.replace({
        name: this.$route.name,
        query: {
          ...this.$route.query,
          displayMode: value,
        }
      });
    },


    setupSkillDevelopmentTreeState(){
      if (this.skillDevelopmentTreeState) {
        const table = document.getElementById("table");
        if (table) {
          this.shownAreas = this.skillDevelopmentTreeState.shownAreas;
          this.shownDirections = this.skillDevelopmentTreeState.shownDirections;
          this.shownSkills = this.skillDevelopmentTreeState.shownSkills;
          this.$nextTick(()=>{
            table.scrollTop = this.skillDevelopmentTreeState.scrollPosition;
          });

        }
      } else {
        for (let area of this.areas) {
          this.shownAreas.push(area.id);
        }
      }
    },
    saveSkillDevelopmentTreeState() {
      const table = document.getElementById("table");

      let scrollPosition = 0;
      if (table) {
        scrollPosition = table.scrollTop;
      }

      this.setSkillDevelopmentTreeState({
        scrollPosition: scrollPosition,
        shownAreas: this.shownAreas,
        shownDirections: this.shownDirections,
        shownSkills: this.shownSkills,
      });
    },
    clearSkillDevelopmentTreeState() {
      this.setSkillDevelopmentTreeState(null);
    },

    toggleArea(areaId) {
      if (this.shownAreas.includes(areaId)) {
        let index = this.shownAreas.findIndex((item)=>{return item==areaId;});
        this.shownAreas.splice(index, 1);
      } else {
        this.shownAreas.push(areaId);
      }
    },
    toggleDirection(directionId) {
      if (this.shownDirections.includes(directionId)) {
        let index = this.shownDirections.findIndex((item)=>{return item==directionId;});
        this.shownDirections.splice(index, 1);
      } else {
        this.shownDirections.push(directionId);
      }
    },
    toggleSkill(skillId) {
      if (this.shownSkills.includes(skillId)) {
        let index = this.shownSkills.findIndex((item)=>{return item==skillId;});
        this.shownSkills.splice(index, 1);
      } else {
        this.shownSkills.push(skillId);
      }
    },

    goToExercise(exerciseId) {
      if (this.reportsStatisticsById[exerciseId]) {
        this.$router.push({
          name: "ExerciseDetails",
          params: { id: exerciseId },
          query: this.$route.query,
        });
      }
    },
  }
};
</script>

<style lang="sass">
.skill-development
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

    .date-range-label
      margin-right: 10px

    .date-range-input
      width: 220px
      text-align: center

.skill-table
  overflow: auto
  height: 100%
  position: relative
  border-top: 1px solid #e8e8e8

  &__body
    border-left: 1px solid #e8e8e8
    border-right: 1px solid #e8e8e8

  &__cell
    padding: 10px 15px
    transition: background 0.3s
    cursor: default
    word-break: break-word
    position: relative
    background-color: #fff

    &:hover
      background: #e6f7ff

    &_sticky
      top: 0
      position: sticky
      position: -webkit-sticky
      background-color: #fff

  &-area
    top: 0
    z-index: 4
    border-bottom: 1px solid #e8e8e8

  &-direction
    top: 42px
    z-index: 3
    border-bottom: 1px solid #e8e8e8
    padding-left: 35px


  &-exercises
    display: flex
    border-bottom: 1px solid #e8e8e8

    &__title
      padding: 10px 15px
      flex: 0 0 10%
      align-self: center

    &__content
      flex: 1 1 90%

.icon-show
  padding: 5px
  margin-right: 5px

  &-hidden
    visibility: hidden

.skill-table__skill-cell
  display: flex
  flex-direction: row
  cursor: default
  top: 83px
  z-index: 2
  border-bottom: 1px solid #e8e8e8
  padding-left: 55px

  &:hover
    background: #e6f7ff

.skill-table__skill__name
  flex: 1
  padding: 10px 0

.skill-table__skill__calls,
.skill-table__skill__mark
  font-weight: bold
  display: flex
  justify-content: center
  align-items: center
  border-left: 1px solid #e8e8e8
  width: 70px

.skill-table__exercise-cell
  display: flex
  flex-direction: row
  cursor: default
  border-top: 1px solid #e8e8e8
  padding-left: 108px

  &:hover
    background: #e6f7ff

  &:first-child
    border-top: 0

.skill-table__exercise-cell__name
  flex: 1
  padding: 10px 0

.exercise-link
  color: #1890ff
  cursor: pointer
  transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1)

  &:hover
    color: #40a9ff

.skill-table__exercise-cell__calls,
.skill-table__exercise-cell__mark
  font-weight: bold
  display: flex
  justify-content: center
  align-items: center
  border-left: 1px solid #e8e8e8
  width: 70px

  &__no-data
    padding: 50px 0
    border: 1px solid #e8e8e8
</style>
