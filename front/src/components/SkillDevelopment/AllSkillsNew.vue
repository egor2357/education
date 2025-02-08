<template>
  <a-spin :spinning="loading">
    <div class="skill-development">
      <div class="top-bar">
        <div class="top-bar__side-block left">
          <a-select
            :value="displayMode"
            @change="changeDisplayMode"
            style="width: 340px"
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

      <div id="table" ref="table" class="skill-table">
        <div>
          <div v-if="filteredAreasByText.length" class="skill-table__body">
            <div v-for="area in filteredAreasByText" :key="area.id">
              <div class="skill-table__cell-container sticky sticky_area">
                <div
                  class="skill-table__cell skill-table__cell_sticky skill-table-area"                
                >
                  <div class="skill-table__cell-wrapper">
                    <a-icon 
                      class="icon-button icon-show"
                      :type="shownAreas.includes(area.id) ? 'down' : 'right'"
                      @click="toggleNode(shownAreas, area.id)"
                    />
                    <text-highlight :queries="searchText">{{ [area.number, area.name].join(". ") }}</text-highlight>
                  </div>
                </div>    
              </div>
              <Transition name="show">
                <div v-if="shownAreas.includes(area.id)">
                  <div v-for="direction in area.children" :key="direction.id">
                    <div class="skill-table__cell-container sticky sticky_direction">
                      <div 
                        class="skill-table__cell"
                        :class="{'skill-table__cell_deleted' : direction.deleted}"
                      >
                        <div class="skill-table__cell-wrapper">  
                          <a-icon
                            class="icon-button icon-show"
                            :type="shownDirections.includes(direction.id) ? 'down' : 'right'"
                            @click="toggleNode(shownDirections, direction.id)"
                          />         
                          <text-highlight :queries="searchText">{{ [area.number, direction.number].join(".") + ". " + direction.name }}</text-highlight>
                        </div>
                      </div>
                    </div>
                                    
                    <Transition name="show">
                      <div v-if="shownDirections.includes(direction.id)">
                        <div v-for="skill in direction.children" :key="skill.id">
                          <div class="skill-table__cell-container sticky sticky_skill">
                            <div
                              class="skill-table__cell"
                              :class="{'skill-table__cell_deleted' : skill.deleted}"
                            >
                              <div class="skill-table__cell-wrapper">
                                <a-icon
                                  class="icon-button icon-show"
                                  :type="shownSkills.includes(skill.id) ? 'down' : 'right'"
                                  @click="toggleNode(shownSkills, skill.id)"
                                />
                                <text-highlight :queries="searchText">{{ [ area.number, direction.number, skill.number].join(".") + ". " + skill.name }}</text-highlight>
                              </div>                                                         
                            </div>
                            <div class="skill-table__mark-bar-container">
                              <a-popover title="Уровень освоения навыка" placement="left">                                          
                                <mark-bar :min=0.33 :max:=1 :value="developedStatistics.skills[skill.id] && developedStatistics.skills[skill.id].value"/>      
                                <template #content>
                                  Количество выполненных упражнений за период: {{ (developedStatistics.skills[skill.id] && developedStatistics.skills[skill.id].called) || 0 }}
                                  <br>
                                  Средняя оценка выполненных упражнений: {{ (developedStatistics.skills[skill.id] && developedStatistics.skills[skill.id].value) || '-' }}
                                </template>  
                              </a-popover>  
                              
                              </div>
                          </div>
                          <Transition name="show">
                            <div v-if="shownSkills.includes(skill.id)">
                              <div v-for="result in skill.children" :key="result.id">
                                <div class="skill-table__cell-container sticky sticky_result">
                                  <div 
                                    class="skill-table__cell skill-table__cell_sticky skill-table-result"
                                    :class="{'skill-table__cell_deleted' : result.deleted}"  
                                  >
                                    <div class="skill-table__cell-wrapper">
                                      <a-icon
                                        class="icon-button icon-show"
                                        :type="shownResults.includes(result.id) ? 'down' : 'right'"
                                        @click="toggleNode(shownResults, result.id)"
                                      />
                                      <text-highlight :queries="searchText">{{ [ area.number, direction.number, skill.number, result.number].join(".") + '. ' + result.name }}</text-highlight>
                                    </div>
                                  </div>
                                  <div class="skill-table__mark-bar-container">
                                    <a-popover title="Уровень достижения ожидаемого результата" placement="left">                                          
                                      <mark-bar :min=0.33 :max:=1 :value="developedStatistics.results[result.id] && developedStatistics.results[result.id].value"/>
                                      <template #content>
                                        Количество выполненных упражнений за период: {{ (developedStatistics.results[result.id] && developedStatistics.results[result.id].called) || 0 }}
                                        <br>
                                        Средняя оценка выполненных упражнений: {{ (developedStatistics.results[result.id] && developedStatistics.results[result.id].value) || '-' }}
                                      </template>  
                                    </a-popover>                                    
                                  </div>
                                </div>
                                <Transition name="show">
                                  <div v-if="shownResults.includes(result.id)">                                    
                                    <div v-for="exercise in result.children" :key="exercise.id"
                                      class="skill-table__cell-container"
                                    >
                                      <div 
                                        class="skill-table__cell skill-table-exercise"
                                        :class="{'skill-table__cell_deleted' : exercise.deleted}"
                                      >
                                        <span
                                          :class="{'exercise-link': developedStatistics.reports[exercise.id]}"
                                          @click="goToExercise(exercise.id)"
                                        >
                                          <text-highlight :queries="searchText">
                                            {{ [ area.number, direction.number, skill.number, result.number, exercise.number].join(".") + '. ' + exercise.name }}
                                          </text-highlight>
                                        </span>  
                                      </div>
                                      <div class="skill-table__mark-bar-container">
                                        
                                        <a-popover title="Оценка диагностического упражненения" placement="left">                                          
                                          <mark-bar :min=0.33 :max:=1 :value="developedStatistics.reports[exercise.id] && developedStatistics.reports[exercise.id].value"/>
                                          <template #content>
                                            Количество выполненных упражнений за период: {{ (developedStatistics.reports[exercise.id] && developedStatistics.reports[exercise.id].called) || 0 }}
                                            <br>
                                            Средняя оценка выполненных упражнений: {{ (developedStatistics.reports[exercise.id] && developedStatistics.reports[exercise.id].value) || '-' }}
                                          </template>  
                                        </a-popover>
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
              </Transition>
            </div>            
          </div>
          <div v-else class="skill-table__no-data">
            <a-empty :image="simpleImage" />
          </div>
        </div>
      </div>
      <div class="bottom-bar">
        <a-input v-model.trim="searchText" placeholder="Поиск" class="search-input" allow-clear/>
      </div>

    </div>
  </a-spin>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from "vuex";
import { Empty } from "ant-design-vue";
import TextHighlight from 'vue-text-highlight';
import moment from "moment";
import { filterBySubstr } from '@/utils/skillStructureFilters';
import MarkBar from '@/components/SkillDevelopment/MarkBar' 

export default {
  components: {
    TextHighlight,
    MarkBar
  },
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
      searchText: '',
      loading: false,

      dateRange: [],
      displayMode: "all",

      reportsStatisticsById: {},
      skillsStatisticsById: {},

      shownAreas: [],
      shownDirections: [],
      shownSkills: [],
      shownResults: [],
    };
  },

  computed: {

    ...mapGetters({
      skillDevelopmentTreeState: "skills/getSkillDevelopmentTreeState",
      developedSkills: "skills/getDevelopedSkills",
      developedPeriod: "skills/getDevelopedPeriod",
      developedStatistics: "skills/getDevelopedStatistics"
    }),

    filteredAreas() {
      let checkFunction;
      if (this.displayMode == "called") {
        checkFunction = (exercise) => {
          return String(exercise.id) in this.developedStatistics.reports;
        }
      } else if (this.displayMode == "notCalled") {
        checkFunction = (exercise) => {
          return !(String(exercise.id) in this.developedStatistics.reports);
        }
      } else {
        checkFunction = (exercise) => {
          return true;
        }
      }

      return this.developedSkills
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
                        results: skill.results
                        .map(result => {
                          return {
                            id: result.id,
                            skill_id: result.skill_id,
                            name: result.name,
                            number: result.number,
                            exercises: result.exercises.filter(checkFunction)
                          }
                        }).filter(result => result.exercises.length)
                      };
                    })
                    .filter(skill => skill.results.length)
                };
              })
              .filter(direction => direction.skills.length)
          };
        })
        .filter(area => area.development_directions.length);
    },

    filteredAreasByText(){
      return filterBySubstr(this.filteredAreas, this.searchText.toLowerCase(), '');
    }
  },

  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },

  async created() {
    if (!this.$route.query.dateFrom) //  Параметров нет, значит, переход был из главного меню
    {      
      this.$router.replace({
        name: this.$route.name,
        query: {
          dateFrom: this.developedPeriod ? this.developedPeriod.start : moment(new Date()).weekday(0).format("YYYY-MM-DD"),
          dateTo: this.developedPeriod ? this.developedPeriod.end : moment(new Date()).weekday(6).format("YYYY-MM-DD"),
          displayMode: this.displayMode
        }
      })
    }
    else // Переход по ссылке либо возврат назад из развития конкретного навыка
    {
      if (this.$route.query.displayMode) {
        this.displayMode = this.$route.query.displayMode;
      }
      this.dateRange.push(moment(this.$route.query.dateFrom));
      this.dateRange.push(moment(this.$route.query.dateTo));
      this.loading = true;
      await this.fetchDevelopedSkills({start: this.dateRange[0].format("YYYY-MM-DD"), end: this.dateRange[1].format("YYYY-MM-DD")});
      this.loading = false; 
      this.setupSkillDevelopmentTreeState();
    }    
  },

  async beforeRouteUpdate(to, from, next) {
    if (from.name != 'ExerciseDetails') {
      this.clearSkillDevelopmentTreeState();
    }

    this.dateRange.splice(0);
    this.dateRange.push(moment(to.query.dateFrom));
    this.dateRange.push(moment(to.query.dateTo));

    if (to.query.displayMode) {
      this.displayMode = to.query.displayMode;
    }
    if (from.query.dateFrom !== to.query.dateFrom || from.query.dateTo !== to.query.dateTo)
    {
      this.loading = true;
      await this.fetchDevelopedSkills({start: to.query.dateFrom, end: to.query.dateTo});
      this.loading = false;
    }
    this.setupSkillDevelopmentTreeState();
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
      fetchDevelopedSkills: "skills/fetchDevelopedSkills"
    }),

    ...mapMutations({
      setSkillDevelopmentTreeState: "skills/setSkillDevelopmentTreeState"
    }),

    toggleNode(shownNodes, nodeId){
      let index = shownNodes.indexOf(nodeId)
      if (index == -1){
        shownNodes.push(nodeId);
      } else {
        shownNodes.splice(index, 1);
      }
    },

    dateRangeChange(value) {
      let queryObj = {
        dateFrom: value[0].format("YYYY-MM-DD"),
        dateTo: value[1].format("YYYY-MM-DD"),
        displayMode: this.displayMode
      };

      this.$router
        .replace({
          name: this.$route.name,
          query: queryObj
        })
        .catch(() => {});
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
        // const table = document.getElementById("table");
        const table = this.$refs.table;
        if (table) {
          this.shownAreas = this.skillDevelopmentTreeState.shownAreas;
          this.shownDirections = this.skillDevelopmentTreeState.shownDirections;
          this.shownSkills = this.skillDevelopmentTreeState.shownSkills;
          this.shownResults = this.skillDevelopmentTreeState.shownResults;
          this.$nextTick(()=>{
            table.scrollTop = this.skillDevelopmentTreeState.scrollPosition;
          });

        }
      } else {
        for (let area of this.developedSkills) {
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
        shownResults: this.shownResults,
      });
    },
    
    clearSkillDevelopmentTreeState() {
      this.setSkillDevelopmentTreeState(null);
    },

    goToExercise(exerciseId) {
      if (this.developedStatistics.reports[exerciseId]) {        
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
mark.text__highlight
  background: #1890ff 
  color: #fff
  padding: 0
</style>

<style lang="sass" scoped>
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

  .bottom-bar
    margin-top: 20px

.sticky
  position: sticky
  position: -webkit-sticky
  background-color: #fff  

  &_area
    top: 0
    z-index: 5

  &_direction
    top: 46px
    z-index: 4
    padding-left: 20px

  &_skill
    top: 92px
    z-index: 3
    padding-left: 40px

  &_result
    top: 138px
    z-index: 2
    padding-left: 60px


.skill-table
  overflow: auto
  height: 100%
  border-top: 1px solid #e8e8e8

  &__body
    border-left: 1px solid #e8e8e8
    border-right: 1px solid #e8e8e8

  &__cell-container
    display: flex
    transition: background .3s
    background: #fff
    border-bottom: 1px solid #e8e8e8

    &:hover
      background: #e6f7ff
    
    .skill-table-exercise
      padding-left: 114px

  &__cell
    padding: 5px 15px
    display: flex
    align-items: center    
    cursor: default
    word-break: break-word    
    min-height: 45px
    flex: 1



  &__cell-wrapper
    line-height: 16px
  
  //&-area
  //  top: 0
  //  z-index: 5
  //  border-bottom: 1px solid #e8e8e8

  //&-direction
  //  top: 45px
  //  z-index: 4
  //  border-bottom: 1px solid #e8e8e8
  //  padding-left: 35px

  //&-skill
  //  top: 90px
  //  z-index: 3
  //  border-bottom: 1px solid #e8e8e8
  //  padding-left: 55px

  //&-result
  //  top: 135px
  //  z-index: 2
  //  border-bottom: 1px solid #e8e8e8
  //  padding-left: 75px

  //&-exercise
  //  border-bottom: 1px solid #e8e8e8
  //  padding-left: 80px

  &__mark-bar-container
    width: 150px
    border-left: 1px solid #e8e8e8
    display: flex
    align-items: center

.icon-show
  margin-right: 5px

.exercise-link
  color: #1890ff
  cursor: pointer
  transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1)

  &:hover
    color: #40a9ff

  &__no-data
    padding: 50px 0
    border: 1px solid #e8e8e8
  
.show-enter-active, .show-leave-active
  transition: opacity 0.3s
  
.show-enter, .show-leave-to
  opacity: 0

mark
  padding: 0 1px
</style>
