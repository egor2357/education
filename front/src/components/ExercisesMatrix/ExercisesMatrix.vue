<template>
  <div class="exercises-matrix-container">
    <a-spin :spinning="loading">
    <div class="specialist-list">
      <a-tag
        class="specialist-label"
        v-for="specialist in specialists" :key="specialist.id"
        :color="
          selectedSpecialists.includes(specialist.id)
          ? specialistToItsMeta[specialist.id].color
          : null
        "
        @click="toggleSpecialistTag(specialist.id)"
      >
        {{
          specialist.surname
          ? formatSpecialist(specialist)
          : specialist.user.username
        }}
      </a-tag>
    </div>
    
    <div class="exercise-specialist-table">
      <div>
        <div v-if="filteredAreas.length" class="exercise-specialist-table__body">
          <div v-for="area in filteredAreas" :key="area.id">
            <div
              class="exercise-specialist-table__cell exercise-specialist-table__cell_sticky exercise-specialist-table-area"
              :class="{'exercise-specialist-table__cell_deleted' : area.deleted}"
            >
              <div class="exercise-specialist-table__cell-wrapper">
                <div class="exercise-specialist-table__cell-label">
                  <a-icon v-if="area.children.length"
                    class="icon-button icon-show"
                    :type="shownAreas.includes(area.id) ? 'down' : 'right'"
                    @click="toggleNode(shownAreas, area.id)"
                  />
                  <span v-else class="placeholder"></span>
                  <text-highlight :queries="searchText">{{ [area.number, area.name].join(". ") }}</text-highlight>
                </div>
                <div class="exercise_specialist_buttons_wrapper">
                  <a-popover title="Добавить упражнения" placement="top">
                    <a-icon
                      @click="setObjectsExercises(
                        'area', area.id, selectedSpecialists,
                        'Упражнения успешно добавлены'
                      )"
                      class="exercise_specialist_button_add_button"
                      :class="{
                        'exercise_specialist_button_disabled': selectedSpecialists.length == 0
                      }"
                      type="pushpin"
                    />
                    <template #content>
                      {{
                        selectedSpecialists.length
                        ? 'Выбранные специалисты смогут контролировать все упражнения этой образовательной области'
                        : 'Ни один специалист не выбран'
                      }}
                    </template>
                  </a-popover>
                  <a-popover title="Убрать упражнения" placement="top">
                    <a-icon
                      @click="removeObjectsExercises(
                        'area', area.id, selectedSpecialists,
                        'Упражнения успешно исключены'
                      )"
                      class="exercise_specialist_button_delete_button"
                      :class="{
                        'exercise_specialist_button_disabled': selectedSpecialists.length == 0
                      }"
                      type="delete"
                    />
                    <template #content>
                      {{
                        selectedSpecialists.length
                        ? 'Выбранные специалисты больше не смогут контролировать упражнения этой образовательной области'
                        : 'Ни один специалист не выбран'
                      }}
                    </template>
                  </a-popover>
                </div>
              </div>
            </div>
            <Transition name="show">
              <div v-if="shownAreas.includes(area.id)">
                <div>
                  <div v-for="direction in area.children" :key="direction.id">
                    <div 
                      class="exercise-specialist-table__cell exercise-specialist-table__cell_sticky exercise-specialist-table-direction"
                      :class="{'exercise-specialist-table__cell_deleted' : direction.deleted}"
                    >
                      <div class="exercise-specialist-table__cell-wrapper">
                        <div class="exercise-specialist-table__cell-label">
                          <a-icon v-if="direction.children.length"
                              class="icon-button icon-show"
                              :type="shownDirections.includes(direction.id) ? 'down' : 'right'"
                              @click="toggleNode(shownDirections, direction.id)"
                            />
                          <span v-else class="placeholder"></span>              
                          <text-highlight :queries="searchText">{{ [area.number, direction.number].join(".") + ". " + direction.name }}</text-highlight>
                        </div>
                        <div class="exercise_specialist_buttons_wrapper">
                          <a-popover title="Добавить упражнения" placement="top">
                            <a-icon
                              @click="setObjectsExercises(
                                'direction', direction.id, selectedSpecialists,
                                'Упражнения успешно добавлены'
                              )"
                              class="exercise_specialist_button_add_button"
                              :class="{
                                'exercise_specialist_button_disabled': selectedSpecialists.length == 0
                              }"
                              type="pushpin"
                            />
                            <template #content>
                              {{
                                selectedSpecialists.length
                                ? 'Выбранные специалисты смогут контролировать все упражнения этого направления развития'
                                : 'Ни один специалист не выбран'
                              }}
                            </template>
                          </a-popover>
                          <a-popover title="Убрать упражнения" placement="top">
                            <a-icon
                              @click="removeObjectsExercises(
                                'direction', direction.id, selectedSpecialists,
                                'Упражнения успешно исключены'
                              )"
                              class="exercise_specialist_button_delete_button"
                              :class="{
                                'exercise_specialist_button_disabled': selectedSpecialists.length == 0
                              }"
                              type="delete"
                            />
                            <template #content>
                              {{
                                selectedSpecialists.length
                                ? 'Выбранные специалисты больше не смогут контролировать упражнения этого направления развития'
                                : 'Ни один специалист не выбран'
                              }}
                            </template>
                          </a-popover>
                        </div>
                      </div>
                    </div>
                                    
                    <Transition name="show">
                      <div v-if="shownDirections.includes(direction.id)">
                        <div>
                          <div v-for="skill in direction.children" :key="skill.id">
                            <div
                              class="exercise-specialist-table__cell exercise-specialist-table__cell_sticky exercise-specialist-table-skill"
                              :class="{'exercise-specialist-table__cell_deleted' : skill.deleted}"
                            >
                              <div class="exercise-specialist-table__cell-wrapper">
                                <div class="exercise-specialist-table__cell-label">
                                  <a-icon v-if="skill.children.length"
                                    class="icon-button icon-show"
                                    :type="shownSkills.includes(skill.id) ? 'down' : 'right'"
                                    @click="toggleNode(shownSkills, skill.id)"
                                  />
                                  <span v-else class="placeholder"></span>
                                  <text-highlight :queries="searchText">{{ [ area.number, direction.number, skill.number].join(".") + ". " + skill.name }}</text-highlight>
                                </div>
                                <div class="exercise_specialist_buttons_wrapper">
                                  <a-popover title="Добавить упражнения" placement="top">
                                    <a-icon
                                      @click="setObjectsExercises(
                                        'skill', skill.id, selectedSpecialists,
                                        'Упражнения успешно добавлены'
                                      )"
                                      class="exercise_specialist_button_add_button"
                                      :class="{
                                        'exercise_specialist_button_disabled': selectedSpecialists.length == 0
                                      }"
                                      type="pushpin"
                                    />
                                    <template #content>
                                      {{
                                        selectedSpecialists.length
                                        ? 'Выбранные специалисты смогут контролировать все упражнения этого навыка'
                                        : 'Ни один специалист не выбран'
                                      }}
                                    </template>
                                  </a-popover>
                                  <a-popover title="Убрать упражнения" placement="top">
                                    <a-icon
                                      @click="removeObjectsExercises(
                                        'skill', skill.id, selectedSpecialists,
                                        'Упражнения успешно исключены'
                                      )"
                                      class="exercise_specialist_button_delete_button"
                                      :class="{
                                        'exercise_specialist_button_disabled': selectedSpecialists.length == 0
                                      }"
                                      type="delete"
                                    />
                                    <template #content>
                                      {{
                                        selectedSpecialists.length
                                        ? 'Выбранные специалисты больше не смогут контролировать упражнения этого навыка'
                                        : 'Ни один специалист не выбран'
                                      }}
                                    </template>
                                  </a-popover>
                                </div>
                              </div>
                            </div>
                            <Transition name="show">
                              <div v-if="shownSkills.includes(skill.id)">
                                <div>
                                  <div v-for="result in skill.children" :key="result.id">
                                    <div 
                                      class="exercise-specialist-table__cell exercise-specialist-table__cell_sticky exercise-specialist-table-result"
                                      :class="{'exercise-specialist-table__cell_deleted' : result.deleted}"  
                                    >
                                      <div class="exercise-specialist-table__cell-wrapper">
                                        <div class="exercise-specialist-table__cell-label">
                                          <a-icon v-if="result.children.length"
                                            class="icon-button icon-show"
                                            :type="shownResults.includes(result.id) ? 'down' : 'right'"
                                            @click="toggleNode(shownResults, result.id)"
                                          />
                                          <span v-else class="placeholder"></span>

                                          <text-highlight :queries="searchText">{{ [ area.number, direction.number, skill.number, result.number].join(".") + '. ' + result.name }}</text-highlight>
                                        </div>
                                        <div class="exercise_specialist_buttons_wrapper">
                                          <a-popover title="Добавить упражнения" placement="top">
                                            <a-icon
                                              @click="setObjectsExercises(
                                                'result', result.id, selectedSpecialists,
                                                'Упражнения успешно добавлены'
                                              )"
                                              class="exercise_specialist_button_add_button"
                                              :class="{
                                                'exercise_specialist_button_disabled': selectedSpecialists.length == 0
                                              }"
                                              type="pushpin"
                                            />
                                            <template #content>
                                              {{
                                                selectedSpecialists.length
                                                ? 'Выбранные специалисты смогут контролировать все упражнения этого ожидаемого результата'
                                                : 'Ни один специалист не выбран'
                                              }}
                                            </template>
                                          </a-popover>
                                          <a-popover title="Убрать упражнения" placement="top">
                                            <a-icon
                                              @click="removeObjectsExercises(
                                                'result', result.id, selectedSpecialists,
                                                'Упражнения успешно исключены'
                                              )"
                                              class="exercise_specialist_button_delete_button"
                                              :class="{
                                                'exercise_specialist_button_disabled': selectedSpecialists.length == 0
                                              }"
                                              type="delete"
                                            />
                                            <template #content>
                                              {{
                                                selectedSpecialists.length
                                                ? 'Выбранные специалисты больше не смогут контролировать упражнения этого ожидаемого результата'
                                                : 'Ни один специалист не выбран'
                                              }}
                                            </template>
                                          </a-popover>
                                        </div>
                                      </div>
                                    </div>
                                    <Transition name="show">
                                    <div v-if="shownResults.includes(result.id)">
                                      <div>
                                        <div v-for="exercise in result.children" :key="exercise.id"
                                          class="exercise-specialist-table__cell exercise-specialist-table-exercise"
                                          :class="{'exercise-specialist-table__cell_deleted' : exercise.deleted}"
                                        >
                                          <text-highlight :queries="searchText">
                                            {{ [ area.number, direction.number, skill.number, result.number, exercise.number].join(".") + '. ' + exercise.name }}
                                          </text-highlight>
                                          <div class="exercise__spectialist__filler"></div>
                                          <template v-if="exercise.id in exerciseToSpecialists">
                                            <div
                                              v-for="specialistId in exerciseToSpecialists[exercise.id]"
                                              :key="specialistId + '.' + exercise.id"
                                              @click="removeObjectsExercises(
                                                'exercise', exercise.id, [specialistId],
                                                'Упражнение успешно исключено'
                                              )"
                                              :style="{
                                                backgroundColor: (selectedSpecialists.includes(specialistId)
                                                  ? specialistToItsMeta[specialistId].color
                                                  : null),
                                                color: (selectedSpecialists.includes(specialistId)
                                                  ? 'white'
                                                  : null),
                                              }"
                                              class="exercise__spectialist__delete_button"
                                            >
                                              <a-popover title="Убрать упражнение" placement="top">
                                              <div                                              
                                                class="exercise__spectialist__delete_button__front"
                                              >
                                                {{ specialistToItsMeta[specialistId].label }}
                                              </div>
                                              <div
                                                class="exercise__spectialist__delete_button__back"
                                              >
                                                <a-icon class="exercise__spectialist__delete_button__close_icon" type="close" />
                                              </div>
                                              <template #content>
                                                Специалист {{ specialistToItsMeta[specialistId].fullLabel }} больше не сможет контролировать выбранное упражнение
                                              </template>
                                              </a-popover>
                                            </div>
                                          </template>
                                          <div class="exercise_specialist_buttons_wrapper">
                                            <a-popover title="Добавить упражнение" placement="top">
                                              <a-icon
                                                @click="setObjectsExercises(
                                                  'exercise', exercise.id, selectedSpecialists,
                                                  'Упражнение успешно добавлено'
                                                )"
                                                class="exercise_specialist_button_add_button"
                                                :class="{
                                                  'exercise_specialist_button_disabled': selectedSpecialists.length == 0
                                                }"
                                                type="pushpin"
                                              />
                                              <template #content>
                                                {{
                                                  selectedSpecialists.length
                                                  ? 'Выбранные специалисты смогут контролировать это упражнение'
                                                  : 'Ни один специалист не выбран'
                                                }}
                                              </template>
                                            </a-popover>
                                            <a-popover title="Убрать упражнение" placement="top">
                                              <a-icon
                                                @click="removeObjectsExercises(
                                                  'exercise', exercise.id, selectedSpecialists,
                                                  'Упражнение успешно исключено'
                                                )"
                                                class="exercise_specialist_button_delete_button"
                                                :class="{
                                                  'exercise_specialist_button_disabled': selectedSpecialists.length == 0
                                                }"
                                                type="delete"
                                              />
                                              <template #content>
                                                {{
                                                  selectedSpecialists.length
                                                  ? 'Выбранные специалисты больше не смогут контролировать это упражнение'
                                                  : 'Ни один специалист не выбран'
                                                }}
                                              </template>
                                            </a-popover>
                                          </div>
                                        </div>
                                      </div>
                                    </div>
                                  </Transition>
                                  </div>
                                </div>
                              </div>
                            </Transition>                          
                          </div>
                        </div>
                      </div>
                    </Transition>
                  </div>
                </div>
              </div>
            </Transition>
          </div>
        </div>
        <div class="exercise-specialist-table__no-data" v-else>
          <a-empty :image="simpleImage" />
        </div>
      </div>
    </div>
    </a-spin>
  </div>
</template>

<script>
const filter = (arr, str, prefix) => (arr || [])
  .map(
    n => (
      {
        name: n.name,
        id: n.id,
        number: n.number,
        deleted: n.deleted,
        children: filter(n.development_directions || n.skills || n.results || n.exercises, (prefix+n.number+'. '+n.name.toLowerCase()).includes(str) ? '' : str, prefix+n.number+'.')
      })
  ).filter(
    n => (prefix+n.number+'. '+n.name.toLowerCase()).includes(str) || n.children.length
  );

import { Empty } from "ant-design-vue";
import TextHighlight from 'vue-text-highlight';
import post from "@/middleware/post";
import { mapActions, mapGetters } from "vuex";
import common from "@/mixins/common";
export default {
  name: "ExercisesMatrix",
  components: {
    TextHighlight,
  },
  mixins: [common],
  props: {
    showMode: {
      type: Number,
      default: 1
    },
    searchText: {
      type: String,
      default: ''
    },
  },
  data() {
    return {
      loading: false,
      shownAreas: [],
      shownDirections: [],
      shownSkills: [],
      shownResults: [],
      colorPresets: [
        '#83A944', '#CC9E08', '#363A57', '#206777', '#FD8A04',
        '#7945BF', '#F46F36', '#AC0E3A', '#264A46', '#266ECA', '#85D0E0',
        '#C82873', '#3AAA07', '#FF5563', '#A95AF3', '#545375', '#D1314B',
        '#FEC305', '#5ACB65', '#203763', '#461234', '#EB4444', '#4F8D08', '#04BDE8', 
      ],
      selectedSpecialists: [],
    };
  },
  async created() {
    this.loading = true;
    await Promise.all([this.fetchSpecialists(), this.fetchAreas()]);
    this.loading = false;
  },
  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },
  methods: {
    ...mapActions({
      fetchSpecialists: "specialists/fetchSpecialists",
      removeExercises: "specialists/removeExercises",
      setExercises: "specialists/setExercises",
      fetchAreas: "skills/fetchAreas",
    }),
    toggleNode(shownNodes, nodeId){
      let index = shownNodes.indexOf(nodeId)
      if (index == -1){
        shownNodes.push(nodeId);
      } else {
        shownNodes.splice(index, 1);
      }
    },
    toggleSpecialistTag (specialistId) {
      if (this.selectedSpecialists.includes(specialistId)) {
        this.selectedSpecialists.splice(this.selectedSpecialists.findIndex(id=>id===specialistId), 1);
      } else {
        this.selectedSpecialists.push(specialistId);
      }
    },
    async setObjectsExercises (objectName, objectId, specialistsIds, successMessage) {
      if (specialistsIds.length === 0) {
        return;
      }
      const successCode = 200;
      let res = await post(
        this.$axios,
        `/api/exercises_to_specialists/set_${objectName}/`,
        {
          [objectName]: objectId,
          specialists: specialistsIds
        }
      );

      if (res.status === successCode) {
        this.$message.success(successMessage);
        this.setExercises({ exercisesIds: res.data.exercises, specialistsIds })
      } else {
        this.$message.error("Произошла ошибка");
      }
    },
    async removeObjectsExercises (objectName, objectId, specialistsIds, successMessage) {
      if (specialistsIds.length === 0) {
        return;
      }
      const successCode = 200;
      let res = await post(
        this.$axios,
        `/api/exercises_to_specialists/remove_${objectName}/`,
        {
          [objectName]: objectId,
          specialists: specialistsIds
        }
      );

      if (res.status === successCode) {
        this.$message.success(successMessage);
        this.removeExercises({ exercisesIds: res.data.exercises, specialistsIds });
      } else {
        this.$message.error("Произошла ошибка");
      }
    },
  },
  computed: {
    ...mapGetters({
      specialists: "specialists/getSpecialists",
      areas: "skills/getAreas",
    }),
    filteredAreas(){
      return filter(this.areas, this.searchText.toLowerCase(), '');
    },
    exerciseToSpecialists () {
      const exerciseToSpecialistsObject = {};
      for (const specialist of this.specialists) {
        if (specialist.exercises.length) {
          for (const exerciseKey of specialist.exercises) {
            if (exerciseKey in exerciseToSpecialistsObject) {
              exerciseToSpecialistsObject[exerciseKey].push(specialist.id);
            } else {
              exerciseToSpecialistsObject[exerciseKey] = [specialist.id];
            }
          }
        }
      }
      return exerciseToSpecialistsObject
    },
    specialistToItsMeta () {
      const specialistToItsMetaObject = {};
      const colorPresetsCount = this.colorPresets.length;
      for (let i=0; i<this.specialists.length; i++) {
        const specialist = this.specialists[i];
        specialistToItsMetaObject[specialist.id] = {
          label: specialist.surname[0].toUpperCase() + specialist.name[0].toUpperCase(),
          fullLabel: this.formatSpecialistFull(specialist),
          color: this.colorPresets[i%colorPresetsCount]
        };
      }
      return specialistToItsMetaObject;
    },
  },
};
</script>

<style lang="sass">
.specialist-list
  padding-bottom: 10px
  display: flex
  flex-direction: row
  flex-wrap: wrap
  gap: 10px

.specialist-label
  font-size: 16px
  padding: 4px 6px
  cursor: pointer
  margin-right: 0

.exercises-matrix-container
  height: 100%
  display: flex
  flex-direction: column

.exercise-specialist-table
  overflow: auto
  height: 100%
  position: relative
  border-top: 1px solid #e8e8e8

  .text__highlight
    background: #1890ff 
    color: #fff

  &__body
    border-left: 1px solid #e8e8e8
    border-right: 1px solid #e8e8e8

  &__cell
    padding: 5px 15px
    display: flex
    align-items: center
    transition: background 0.3s
    cursor: default
    word-break: break-word
    position: relative
    background-color: #fff
    min-height: 45px

    &_deleted
      text-decoration: line-through
      color: #999

    .icon-show
      margin-right: 5px

    i.icon-actions
      height: 16px
      font-size: 16px
      display: none
      position: absolute
      right: 5px
      cursor: pointer
      top: 13px

    .placeholder
      padding-left: 19px

    &:hover
      background: #e6f7ff

      i.icon-actions
        display: inherit

    &_sticky
      top: 0
      position: sticky
      position: -webkit-sticky
      background-color: #fff

  &__cell-wrapper
    line-height: 16px
    width: 100%
    display: flex
    flex-direction: row

  &__cell-label
    flex: 1

  &-area
    top: 0
    z-index: 5
    border-bottom: 1px solid #e8e8e8

  &-direction
    top: 45px
    z-index: 4
    border-bottom: 1px solid #e8e8e8
    padding-left: 35px

  &-skill
    top: 90px
    z-index: 3
    border-bottom: 1px solid #e8e8e8
    padding-left: 55px

  &-result
    top: 135px
    z-index: 2
    border-bottom: 1px solid #e8e8e8
    padding-left: 75px

  &-exercise
    border-bottom: 1px solid #e8e8e8
    padding-left: 114px

    &__title
      padding: 10px 15px
      flex: 0 0 10%
      align-self: center

    &__content
      flex: 1 1 90%

      .exercise-specialist-table__cell
        padding-left: 108px
        border-top: 1px solid #e8e8e8
        &:first-child
          border-top: 0

  &__no-data
    padding: 50px 0
    border: 1px solid #e8e8e8

.show-enter-active, .show-leave-active
  transition: opacity 0.3s

.show-enter, .show-leave-to
  opacity: 0

.exercise__spectialist__filler
  flex-grow: 1

.exercise__spectialist__delete_button
  width: 30px
  height: 30px
  overflow: hidden
  border-radius: 15px
  position: relative
  cursor: pointer
  margin-left: 6px
  color: rgba(0, 0, 0, 0.65)
  border: 1px solid #d9d9d9
  background-color: #fff

.exercise__spectialist__delete_button__front
  width: 100%
  height: 100%
  display: flex
  align-items: center
  justify-content: center
  transition: opacity 0.3s
  
.exercise__spectialist__delete_button__back
  opacity: 0
  position: absolute
  width: 100%
  height: 100%
  z-index: 10
  top: 0
  left: 0
  display: flex
  align-items: center
  justify-content: center
  transition: opacity 0.3s
.exercise__spectialist__delete_button:hover .exercise__spectialist__delete_button__back
  opacity: 1
.exercise__spectialist__delete_button:hover .exercise__spectialist__delete_button__front
  opacity: 0

.exercise_specialist_buttons_wrapper
  display: flex
  flex-direction: row
  align-items: center
  justify-content: center
  width: 50px
  margin-left: 20px
.exercise_specialist_button_add_button
  margin-right: 10px
  color: red
.exercise_specialist_button_delete_button
  color: #40a9ff
.exercise_specialist_button_add_button, .exercise_specialist_button_delete_button
  cursor: pointer
  opacity: 0.6
.exercise_specialist_button_add_button:hover, .exercise_specialist_button_delete_button:hover
  opacity: 1
.exercise_specialist_button_disabled
  cursor: default
  color: #a2a2a2
  opacity: 1  
.exercise-specialist-table__cell-wrapper .exercise_specialist_buttons_wrapper
  opacity: 0
.exercise-specialist-table__cell-wrapper:hover .exercise_specialist_buttons_wrapper
  opacity: 1

</style>
