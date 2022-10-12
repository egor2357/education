<template>
  <div class="skill-table">
    <div>
      <div v-if="areas.length" class="skill-table__body">
        <div v-for="area in areas" :key="area.id">
          <div
            class="skill-table__cell skill-table__cell_sticky skill-table-area"
          >
            <a-icon
              class="icon-button icon-show"
              :type="shownAreas.includes(area.id) ? 'down' : 'right'"
              @click="toggleArea(area.id)"
            />
            <span
              >
              {{ [area.number, area.name].join(". ") }}</span
            >
            <a-dropdown
              :trigger="['click']"
              placement="bottomLeft"
              class="dropdown--hover"
            >
              <a-icon class="icon-button icon-actions" type="more"></a-icon>
              <a-menu slot="overlay">
                <a-menu-item
                  key="0"
                  @click="$emit('onAddItem', { type: 2, item: area })"
                >
                  Добавить направление развития
                </a-menu-item>
                <a-menu-item
                  key="1"
                  @click="$emit('onEditItem', { type: 1, item: area })"
                >
                  Изменить
                </a-menu-item>
                <a-menu-item
                  key="2"
                  @click="
                    $emit('onDeleteItem', {
                      id: area.id,
                      name: [area.number, area.name].join('. '),
                      type: 1
                    })
                  "
                >
                  <span> Удалить </span>
                </a-menu-item>
              </a-menu>
            </a-dropdown>
          </div>
          <Transition name="show">
            <div v-if="shownAreas.includes(area.id)" class="skill-table-direction-wrapper">
              <div
                class="skill-table__cell skill-table__cell_sticky"
                v-if="!area.development_directions.length"
              >
                <a @click="$emit('onAddItem', { type: 2, item: area })"
                  >Добавить направление развития</a
                >
              </div>
              <template v-else>
                <div
                  v-for="direction in area.development_directions"
                  :key="direction.id"
                >
                  <div
                    class="skill-table__cell skill-table__cell_sticky skill-table-direction"
                  >
                    <a-icon
                      class="icon-button icon-show"
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
                    <a-dropdown
                      :trigger="['click']"
                      placement="bottomLeft"
                      class="dropdown--hover"
                    >
                      <a-icon
                        class="icon-button icon-actions"
                        type="more"
                      ></a-icon>
                      <a-menu slot="overlay">
                        <a-menu-item
                          key="0"
                          @click="
                            $emit('onAddItem', { type: 3, item: direction })
                          "
                        >
                          Добавить навык
                        </a-menu-item>
                        <a-menu-item
                          key="1"
                          @click="
                            $emit('onEditItem', { type: 2, item: direction })
                          "
                        >
                          Изменить
                        </a-menu-item>
                        <a-menu-item
                          key="2"
                          @click="
                            $emit('onDeleteItem', {
                              id: direction.id,
                              name:
                                [area.number, direction.number].join('.') +
                                '. ' +
                                direction.name,
                              type: 2
                            })
                          "
                        >
                          <span> Удалить </span>
                        </a-menu-item>
                      </a-menu>
                    </a-dropdown>
                  </div>
                  <Transition name="show">
                    <div v-if="shownDirections.includes(direction.id)">
                      <div
                        v-if="!direction.skills.length"
                        class="skill-table__cell"
                      >
                        <a
                          @click="$emit('onAddItem', { type: 3, item: direction })"
                        >
                          Добавить навык
                        </a>
                      </div>
                      <div v-else>
                        <div v-for="skill in direction.skills" :key="skill.id">
                          <div
                            class="skill-table__cell skill-table__cell_sticky skill-table-skill"
                          >
                            <a-icon
                              class="icon-button icon-show"
                              :type="shownSkills.includes(skill.id) ? 'down' : 'right'"
                              @click="toggleSkill(skill.id)"
                            />
                            <span>
                              {{ [ area.number, direction.number, skill.number].join(".") +
                                  ". " + skill.name }}
                            </span>
                            <a-dropdown
                              :trigger="['click']"
                              placement="bottomLeft"
                              class="dropdown--hover"
                            >
                              <a-icon
                                class="icon-button icon-actions"
                                type="more"
                              ></a-icon>
                              <a-menu slot="overlay">
                                <a-menu-item
                                  key="0"
                                  @click="
                                    $emit('onAddItem', { type: 4, item: skill })
                                  "
                                >
                                  Добавить упражнение
                                </a-menu-item>
                                <a-menu-item
                                  key="1"
                                  @click="$emit('onEditItem', { type: 3, item: skill })"
                                >
                                  Изменить
                                </a-menu-item>
                                <a-menu-item
                                  key="2"
                                  @click="
                                    $emit('onDeleteItem', {
                                      id: skill.id,
                                      name:
                                        [
                                          area.number,
                                          direction.number,
                                          skill.number
                                        ].join('.') +
                                        '. ' +
                                        skill.name,
                                      type: 3
                                    })
                                  "
                                >
                                  <span> Удалить </span>
                                </a-menu-item>
                              </a-menu>
                            </a-dropdown>
                          </div>
                          <Transition name="show">
                            <div
                              v-if="shownSkills.includes(skill.id)"
                              class="skill-table-exercises"
                            >
                              <div class="skill-table-exercises__content">
                                <div
                                  v-if="!skill.exercises.length"
                                  class="skill-table__cell"
                                >
                                  <a @click="$emit('onAddItem', {type: 4, item: skill})">
                                    Добавить упражнение
                                  </a>
                                </div>
                                <div v-else>
                                  <div
                                    v-for="exercise in skill.exercises"
                                    :key="exercise.id"
                                    class="skill-table__cell"
                                  >
                                    <span>
                                      {{
                                        [ area.number, direction.number, skill.number, exercise.number].join(".") +
                                        '. ' + exercise.name
                                      }}
                                    </span>
                                    <a-dropdown
                                      :trigger="['click']"
                                      placement="bottomLeft"
                                      class="dropdown--hover"
                                    >
                                      <a-icon
                                        class="icon-button icon-actions"
                                        type="more"
                                      ></a-icon>
                                      <a-menu slot="overlay">
                                        <a-menu-item
                                          key="1"
                                          @click="$emit('onEditItem', { type: 4, item: exercise })"
                                        >
                                          Изменить
                                        </a-menu-item>
                                        <a-menu-item
                                          key="2"
                                          @click="
                                            $emit('onDeleteItem', {
                                              id: exercise.id,
                                              name:
                                                [
                                                  area.number,
                                                  direction.number,
                                                  skill.number,
                                                  exercise.number
                                                ].join('.') +
                                                '. ' +
                                                exercise.name,
                                              type: 4
                                            })
                                          "
                                        >
                                          <span> Удалить </span>
                                        </a-menu-item>
                                      </a-menu>
                                    </a-dropdown>
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
              </template>
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
import { Empty } from "ant-design-vue";
export default {
  name: "SkillsTable",
  props: {
    areas: {
      type: Array,
      default() {
        return [];
      },
      loading: {
        type: Boolean,
        default: false
      }
    }
  },
  data() {
    return {
      shownAreas: [],
      shownDirections: [],
      shownSkills: [],
    };
  },
  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },
  methods: {
    initShownAreas() {
      for (let area of this.areas) {
        this.shownAreas.push(area.id);
      }
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
  }
};
</script>

<style lang="sass">
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

    .icon-show
      padding: 5px
      margin-right: 5px

    i.icon-actions
      height: 16px
      font-size: 16px
      display: none
      position: absolute
      right: 5px
      cursor: pointer
      top: 13px

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

  &-exercises
    display: flex
    border-bottom: 1px solid #e8e8e8

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

.show-enter-active, .show-leave-active
  transition: opacity 0.3s

.show-enter, .show-leave-to
  opacity: 0
</style>
