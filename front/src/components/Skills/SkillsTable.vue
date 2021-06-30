<template>
  <div class="skill-table">
    <div>
      <div class="skill-table__header">
        <div class="skill-table__cell area">
          <div class="skill-table__cell-label">Образовательная область</div>
        </div>
        <div class="skill-table__cell direction">
          <div class="skill-table__cell-label">Направление развития</div>
        </div>
        <div class="skill-table__cell skill">
          <div class="skill-table__cell-label">Навык</div>
        </div>
      </div>
      <div class="skill-table__body" v-if="tableData.length">
        <div
          class="skill-table__area-row"
          v-for="area in tableData"
          :key="area.id"
        >
          <div class="skill-table__cell area">
            <div class="skill-table__cell-label">
              <span class="skill-table__cell-label-text"
                >{{ [area.number, area.name].join(". ") }}
                <a-dropdown
                  :trigger="['click']"
                  placement="bottomLeft"
                  class="dropdown--hover"
                >
                  <a-icon class="icon-button" type="more"></a-icon>
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
                          type: 1,
                        })
                      "
                    >
                      <span> Удалить </span>
                    </a-menu-item>
                  </a-menu>
                </a-dropdown>
              </span>
            </div>
          </div>
          <div class="skill-table__area-directions">
            <div
              class="skill-table__direction-row"
              v-if="!area.development_directions.length"
            >
              <div class="skill-table__cell direction"></div>
              <div class="skill-table__direction-skills">
                <div class="skill-table__cell skill"></div>
              </div>
            </div>
            <div
              class="skill-table__direction-row"
              v-for="direction in area.development_directions"
              :key="direction.id"
            >
              <div class="skill-table__cell direction">
                <div class="skill-table__cell-label">
                  <span class="skill-table__cell-label-text">
                    {{
                      [area.number, direction.number].join(".") +
                      ". " +
                      direction.name
                    }}
                    <a-dropdown
                      :trigger="['click']"
                      placement="bottomLeft"
                      class="dropdown--hover"
                    >
                      <a-icon class="icon-button" type="more"></a-icon>
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
                              type: 2,
                            })
                          "
                        >
                          <span> Удалить </span>
                        </a-menu-item>
                      </a-menu>
                    </a-dropdown>
                  </span>
                </div>
              </div>
              <div class="skill-table__direction-skills">
                <div
                  class="skill-table__cell skill"
                  v-if="!direction.skills.length"
                ></div>
                <div
                  class="skill-table__skill-row"
                  v-for="skill in direction.skills"
                  :key="skill.id"
                >
                  <div class="skill-table__cell skill">
                    <div class="skill-table__cell-label">
                      <span class="skill-table__cell-label-text">
                        {{
                          [area.number, direction.number, skill.number].join(
                            "."
                          ) +
                          ". " +
                          skill.name
                        }}
                        <a-dropdown
                          :trigger="['click']"
                          placement="bottomLeft"
                          class="dropdown--hover"
                        >
                          <a-icon class="icon-button" type="more"></a-icon>
                          <a-menu slot="overlay">
                            <a-menu-item
                              key="1"
                              @click="
                                $emit('onEditItem', { type: 3, item: skill })
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
                                      skill.number,
                                    ].join('.') +
                                    '. ' +
                                    skill.name,
                                  type: 3,
                                })
                              "
                            >
                              <span> Удалить </span>
                            </a-menu-item>
                          </a-menu>
                        </a-dropdown>
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
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
        default: false,
      },
    },
  },
  data() {
    return {};
  },
  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },
};
</script>

<style lang="sass">
.skill-table
  overflow: auto
  height: 100%
  position: relative

.skill-table__cell
  transition: background 0.3s
  cursor: default

  &.area
    width: 20%

  &.direction
    border-left: 1px solid #e8e8e8

  &.skill
    border-left: 1px solid #e8e8e8
    flex: 1

.skill-table__header
  display: flex
  border: 1px solid #e8e8e8
  background: #fafafa
  position: sticky
  position: -webkit-sticky
  top: 0
  z-index: 3
  line-height: 20px
  height: 42px

  .skill-table__cell.direction
    width: 20%
    border-left: 1px solid #e8e8e8

.skill-table__body
  border: 1px solid #e8e8e8
  border-top: 0 none

  .skill-table__cell.direction
    width: 25%

  .skill-table__cell:hover
    background: #e6f7ff

    i
      display: inherit

.skill-table__area-directions
  display: flex
  flex-direction: column
  flex: 1

.skill-table__direction-skills
  display: flex
  flex-direction: column
  flex: 1

.skill-table__area-row, .skill-table__direction-row, .skill-table__skill-row
  display: flex
  border-top: 1px solid #e8e8e8
  flex: 1 1 auto

.skill-table__area-row:first-child, .skill-table__direction-row:first-child, .skill-table__skill-row:first-child
  border-top: 0 none

.skill-table__cell-label
  padding: 10px 15px
  position: sticky
  position: -webkit-sticky
  top: 42px
  z-index: 1

  .skill-table__cell-label-text
    display: flex
    word-break: break-word

    i
      height: 16px
      font-size: 16px
      display: none
      position: absolute
      right: 5px
      cursor: pointer
      top: 10px

.skill-table__no-data
  padding: 50px 0
  border: 1px solid #e8e8e8
  border-top: 0 none
</style>
