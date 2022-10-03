<template>
  <div class="skill-table">
    <div>
      <div v-if="tableData.length" class="skill-table__body">
        <div v-for="area in tableData" :key="area.id">
          <div
            class="skill-table__cell skill-table__cell_sticky skill-table-area"
          >
            <a-icon
              class="icon-button icon-show"
              :type="showArea[area.id] ? 'caret-down' : 'caret-right'"
              @click="showArea[area.id] = !showArea[area.id]"
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
            <div v-if="showArea[area.id]" class="skill-table-direction-wrapper">
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
                      :type="
                        showDirection[direction.id] ? 'caret-down' : 'caret-right'
                      "
                      @click="
                        showDirection[direction.id] = !showDirection[
                          direction.id
                        ]
                      "
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
                    <div v-if="showDirection[direction.id]">
                      <div
                        v-if="!direction.skills.length"
                        class="skill-table__cell"
                      >
                        <a
                          @click="
                            $emit('onAddItem', { type: 3, item: direction })
                          "
                          >Добавить навык</a
                        >
                      </div>
                      <div v-else>
                        <div v-for="skill in direction.skills" :key="skill.id">
                          <div
                            class="skill-table__cell skill-table__cell_sticky skill-table-skill"
                          >
                            <a-icon
                              class="icon-button icon-show"
                              :type="
                                showSkill[skill.id] ? 'caret-down' : 'caret-right'
                              "
                              @click="
                                showSkill[skill.id] = !showSkill[skill.id]
                              "
                            />
                            <span>
                              {{
                                [
                                  area.number,
                                  direction.number,
                                  skill.number
                                ].join(".") +
                                  ". " +
                                  skill.name
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
                                    $emit('onAddItem', { type: 4, item: skill })
                                  "
                                >
                                  Добавить упражнение
                                </a-menu-item>
                                <a-menu-item
                                  key="1"
                                  @click="
                                    $emit('onEditItem', {
                                      type: 3,
                                      item: skill
                                    })
                                  "
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
                              v-if="showSkill[skill.id]"
                              class="skill-table-exercises"
                            >
                              <div class="skill-table-exercises__content">
<!--                                <div-->
<!--                                  v-if="!skill.exercises.length"-->
<!--                                  class="skill-table__cell"-->
<!--                                >-->
<!--                                  <a-->
<!--                                    @click="-->
<!--                                      $emit('onAddItem', {-->
<!--                                        type: 4,-->
<!--                                        item: skill-->
<!--                                      })-->
<!--                                    "-->
<!--                                    >Добавить упражнение</a-->
<!--                                  >-->
<!--                                </div>-->
                                <div>
                                  <div
                                    v-for="i in 3"
                                    :key="i"
                                    class="skill-table__cell"
                                  >
                                    <span>1.2.10.1 Броски {{ i }}</span>
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
                                          @click="
                                            $emit('onEditItem', {
                                              type: 4,
                                              item: exercise
                                            })
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
    tableData: {
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
      showArea: {},
      showDirection: {},
      showSkill: {}
    };
  },
  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },
  methods: {
    prepareObjects() {
      this.tableData.forEach(area => {
        this.$set(this.showArea, area.id, true);
        area.development_directions.forEach(direction => {
          this.$set(this.showDirection, direction.id, false);
          direction.skills.forEach(skill => {
            this.$set(this.showSkill, skill.id, false);
          });
        });
      });
    }
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
    top: 42px
    z-index: 3
    border-bottom: 1px solid #e8e8e8
    padding-left: 35px

  &-skill
    top: 83px
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
        padding-left: 90px
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
