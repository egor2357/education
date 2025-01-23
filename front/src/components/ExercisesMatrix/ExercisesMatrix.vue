<template>
  <div class="exercises-matrix-container">
    <div class="specialist-list">
      <a-tag
        color="green"
        class="specialist-label"
        v-for="specialist in specialists" :key="specialist.id"
      >
        {{
          specialist.surname
          ? formatSpecialist(specialist)
          : specialist.user.username
        }}
      </a-tag>
    </div>
    <div class="skill-table">
      <div v-if="filteredAreas.length" class="skill-table__body">
        <div v-for="area in filteredAreas" :key="area.id">
          <div
            class="skill-table__cell skill-table__cell_sticky skill-table-area"
            :class="{'skill-table__cell_deleted' : area.deleted}"
          >
            <a-icon v-if="!area.deleted || area.children.length"
              class="icon-button icon-show"
              :type="shownAreas.includes(area.id) ? 'down' : 'right'"
              @click="toggleNode(shownAreas, area.id)"
            />
            <span v-else class="placeholder"></span>
            <text-highlight :queries="searchText">{{ [area.number, area.name].join(". ") }}</text-highlight>

          </div>
          <Transition name="show">
            <div v-if="shownAreas.includes(area.id)">
              <div>
                <div v-for="direction in area.children" :key="direction.id">
                  <div
                    class="skill-table__cell skill-table__cell_sticky skill-table-direction"
                    :class="{'skill-table__cell_deleted' : direction.deleted}"
                  >
                    <a-icon v-if="!direction.deleted || direction.children.length"
                      class="icon-button icon-show"
                      :type="shownDirections.includes(direction.id) ? 'down' : 'right'"
                      @click="toggleNode(shownDirections, direction.id)"
                    />
                    <span v-else class="placeholder"></span>
                    <text-highlight :queries="searchText">{{ [area.number, direction.number].join(".") + ". " + direction.name }}</text-highlight>

                  </div>
                  <Transition name="show">
                    <div v-if="shownDirections.includes(direction.id)">
                      <div>
                        <div v-for="skill in direction.children" :key="skill.id">
                          <div
                            class="skill-table__cell skill-table__cell_sticky skill-table-skill"
                            :class="{'skill-table__cell_deleted' : skill.deleted}"
                          >
                            <a-icon v-if="!skill.deleted || skill.children.length"
                              class="icon-button icon-show"
                              :type="shownSkills.includes(skill.id) ? 'down' : 'right'"
                              @click="toggleNode(shownSkills, skill.id)"
                            />
                            <span v-else class="placeholder"></span>
                            <text-highlight :queries="searchText">{{ [ area.number, direction.number, skill.number].join(".") + ". " + skill.name }}</text-highlight>

                          </div>
                          <Transition name="show">
                            <div v-if="shownSkills.includes(skill.id)">
                              <div>
                                <div v-for="result in skill.children" :key="result.id">
                                  <div
                                    class="skill-table__cell skill-table__cell_sticky skill-table-result"
                                    :class="{'skill-table__cell_deleted' : result.deleted}"
                                  >
                                    <a-icon v-if="!result.deleted || result.children.length"
                                      class="icon-button icon-show"
                                      :type="shownResults.includes(result.id) ? 'down' : 'right'"
                                      @click="toggleNode(shownResults, result.id)"
                                    />
                                    <span v-else class="placeholder"></span>

                                    <text-highlight :queries="searchText">{{ [ area.number, direction.number, skill.number, result.number].join(".") + '. ' + result.name }}</text-highlight>

                                  </div>
                                  <Transition name="show">
                                  <div v-if="shownResults.includes(result.id)">
                                    <div>
                                      <div v-for="exercise in result.children" :key="exercise.id"
                                        class="skill-table__cell skill-table__cell_sticky skill-table-exercise"
                                        :class="{'skill-table__cell_deleted' : exercise.deleted}"
                                      >
                                        <text-highlight :queries="searchText" class="skill-table-exercise-name">
                                          {{ [ area.number, direction.number, skill.number, result.number, exercise.number].join(".") + '. ' + exercise.name }}
                                        </text-highlight>
                                        <div class="exercise__spectialist__flip_button">
                                          <div class="exercise__spectialist__flip_button__inner">
                                            <a-button
                                              type="primary" shape="circle" size="small"
                                              class="exercise__spectialist__flip_button__front"
                                            >
                                              AВ
                                            </a-button>
                                            <a-button
                                              type="primary" shape="circle" size="small"
                                              class="exercise__spectialist__flip_button__back"
                                            >
                                              X
                                            </a-button>
                                          </div>
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
      <div class="skill-table__no-data" v-else>
        <a-empty :image="simpleImage" />
      </div>
    </div>


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
import { mapActions, mapGetters } from "vuex";
import common from "@/mixins/common";
export default {
  name: "ExercisesMatrix",
  components: {
    TextHighlight,
  },
  mixins: [common],
  data() {
    return {
      loading: false,
      shownAreas: [],
      shownDirections: [],
      shownSkills: [],
      shownResults: [],
      searchText: '',
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
  },
  computed: {
    ...mapGetters({
      specialists: "specialists/getSpecialists",
      specialistsFetched: "specialists/getFetched",
      areas: "skills/getAreas",
    }),
    filteredAreas(){
      return filter(this.areas, this.searchText.toLowerCase(), '');
    }
  },
};
</script>

<style lang="sass">
.exercises-matrix-container
  height: 100%
  display: flex
  flex-direction: column

.specialist-list
  padding-bottom: 10px

.skill-table
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
    padding: 10px 15px
    transition: background 0.3s
    cursor: default
    word-break: break-word
    position: relative
    background-color: #fff

    &_deleted
      text-decoration: line-through
      color: #999

    .icon-show
      padding: 5px 0
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

  &-area
    top: 0
    z-index: 4
    border-bottom: 1px solid #e8e8e8

  &-direction
    top: 45px
    z-index: 3
    border-bottom: 1px solid #e8e8e8
    padding-left: 35px

  &-skill
    top: 90px
    z-index: 2
    border-bottom: 1px solid #e8e8e8
    padding-left: 55px

  &-result
    top: 90px
    z-index: 2
    border-bottom: 1px solid #e8e8e8
    padding-left: 75px

  &-exercise
    display: flex
    top: 90px
    z-index: 2
    border-bottom: 1px solid #e8e8e8
    padding-left: 114px

    &__title
      padding: 10px 15px
      flex: 0 0 10%
      align-self: center

    &__content
      flex: 1 1 90%

      .skill-table__cell
        padding-left: 108px
        border-top: 1px solid #e8e8e8
        &:first-child
          border-top: 0

  &__no-data
    padding: 50px 0
    border: 1px solid #e8e8e8

.exercise__spectialist__flip_button
  background-color: transparent

/* This container is needed to position the front and back side */
.exercise__spectialist__flip_button__inner
  position: relative
  width: 100%
  height: 100%
  text-align: center
  transition: transform 0.8s
  transform-style: preserve-3d

/* Do an horizontal flip when you move the mouse over the flip box container */
.exercise__spectialist__flip_button:hover .exercise__spectialist__flip_button__inner
  transform: rotateY(180deg)

/* Position the front and back side */
.exercise__spectialist__flip_button__front, .exercise__spectialist__flip_button__back
  position: absolute
  width: 100%
  height: 100%
  -webkit-backface-visibility: hidden /* Safari */
  backface-visibility: hidden

/* Style the back side */
.exercise__spectialist__flip_button__back
  transform: rotateY(180deg)

</style>
