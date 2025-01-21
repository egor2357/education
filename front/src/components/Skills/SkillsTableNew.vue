<template>  
  <div class="skill-table">
    <div>
      <div v-if="filteredAreas.length" class="skill-table__body">
        <div v-for="area in filteredAreas" :key="area.id">
          <div
            class="skill-table__cell skill-table__cell_sticky skill-table-area"
          >
            <a-icon
              class="icon-button icon-show"
              :type="shownAreas.includes(area.id) ? 'down' : 'right'"
              @click="toggleNode(shownAreas, area.id)"
            />
            <!-- <span>{{ [area.number, area.name].join(". ") }}</span> -->
            <text-highlight :queries="searchText">{{ [area.number, area.name].join(". ") }}</text-highlight>
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
            <div v-if="shownAreas.includes(area.id)">
              <div
                class="skill-table__cell skill-table__cell_sticky skill-table-direction"
                v-if="!area.children.length"
              >
                <a @click="$emit('onAddItem', { type: 2, item: area })">Добавить направление развития</a>
              </div>
              <div v-else>
                <div v-for="direction in area.children" :key="direction.id">
                  <div class="skill-table__cell skill-table__cell_sticky skill-table-direction">
                    <a-icon
                      class="icon-button icon-show"
                      :type="shownDirections.includes(direction.id) ? 'down' : 'right'"
                      @click="toggleNode(shownDirections, direction.id)"
                    />
                    <!-- <span>
                      {{
                        [area.number, direction.number].join(".") +
                          ". " +
                          direction.name
                      }}
                    </span> -->
                    <text-highlight :queries="searchText">{{ [area.number, direction.number].join(".") + ". " + direction.name }}</text-highlight>
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
                        v-if="!direction.children.length"
                        class="skill-table__cell skill-table__cell_sticky skill-table-skill"
                      >
                        <a
                          @click="$emit('onAddItem', { type: 3, item: direction })"
                        >
                          Добавить навык
                        </a>
                      </div>
                      <div v-else>
                        <div v-for="skill in direction.children" :key="skill.id">
                          <div
                            class="skill-table__cell skill-table__cell_sticky skill-table-skill"
                          >
                            <a-icon
                              class="icon-button icon-show"
                              :type="shownSkills.includes(skill.id) ? 'down' : 'right'"
                              @click="toggleNode(shownSkills, skill.id)"
                            />
                            <!-- <span>
                              {{ [ area.number, direction.number, skill.number].join(".") +
                                  ". " + skill.name }}
                            </span> -->
                            <text-highlight :queries="searchText">{{ [ area.number, direction.number, skill.number].join(".") + ". " + skill.name }}</text-highlight>
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
                                  Добавить ожидаемый результат
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
                            <div v-if="shownSkills.includes(skill.id)">
                              <div
                                v-if="!skill.children.length"
                                class="skill-table__cell skill-table__cell_sticky skill-table-result"
                              >
                                <a @click="$emit('onAddItem', {type: 4, item: skill})">
                                  Добавить ожидаемый результат
                                </a>
                              </div>
                              <div v-else>
                                <div v-for="result in skill.children" :key="result.id">
                                  <div class="skill-table__cell skill-table__cell_sticky skill-table-result">
                                    <a-icon
                                      class="icon-button icon-show"
                                      :type="shownResults.includes(result.id) ? 'down' : 'right'"
                                      @click="toggleNode(shownResults, result.id)"
                                    />
                                    <!-- <span>
                                      {{
                                        [ area.number, direction.number, skill.number, result.number].join(".") +
                                        '. ' + result.name
                                      }}
                                    </span> -->
                                    <text-highlight :queries="searchText">{{ [ area.number, direction.number, skill.number, result.number].join(".") + '. ' + result.name }}</text-highlight>
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
                                            $emit('onAddItem', { type: 5, item: result })
                                          "
                                        >
                                          Добавить диагностическое упражнение
                                        </a-menu-item>
                                        <a-menu-item
                                          key="1"
                                          @click="$emit('onEditItem', { type: 4, item: result })"
                                        >
                                          Изменить
                                        </a-menu-item>
                                        <a-menu-item
                                          key="2"
                                          @click="
                                            $emit('onDeleteItem', {
                                              id: result.id,
                                              name:
                                                [
                                                  area.number,
                                                  direction.number,
                                                  skill.number,
                                                  result.number
                                                ].join('.') +
                                                '. ' +
                                                result.name,
                                              type: 4
                                            })
                                          "
                                        >
                                          <span> Удалить </span>
                                        </a-menu-item>
                                      </a-menu>
                                    </a-dropdown>
                                  </div>
                                  <Transition name="show">
                                  <div v-if="shownResults.includes(result.id)">
                                    <div
                                      v-if="!result.children.length"
                                      class="skill-table__cell skill-table__cell_sticky skill-table-exercise"
                                    >
                                      <a @click="$emit('onAddItem', {type: 5, item: result})">
                                        Добавить диагностическое упражнение
                                      </a>
                                    </div>
                                    <div v-else>
                                      <div v-for="exercise in result.children" :key="exercise.id"
                                        class="skill-table__cell skill-table__cell_sticky skill-table-exercise"
                                      >
                                        <!-- <span>
                                          {{
                                            [ area.number, direction.number, skill.number, result.number, exercise.number].join(".") +
                                            '. ' + exercise.name
                                          }}
                                        </span> -->
                                        <text-highlight :queries="searchText">{{ [ area.number, direction.number, skill.number, result.number, exercise.number].join(".") + '. ' + exercise.name }}</text-highlight>
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
                                              @click="$emit('onEditItem', { type: 5, item: exercise })"
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
                                                      result.number,
                                                      exercise.number
                                                    ].join('.') +
                                                    '. ' +
                                                    exercise.name,
                                                  type: 5
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
import { Empty } from "ant-design-vue";
import TextHighlight from 'vue-text-highlight';

const filter = (arr, str, prefix) => (arr || [])
  .map(
    n => (
      { 
        name: n.name, 
        id: n.id, 
        number: n.number, 
        children: filter(n.development_directions || n.skills || n.results || n.exercises, (prefix+n.number+'. '+n.name.toLowerCase()).includes(str) ? '' : str, prefix+n.number+'.') 
      })
  ).filter(
    n => (prefix+n.number+'. '+n.name.toLowerCase()).includes(str) || n.children.length
  );

export default {
  name: "SkillsTable",
  components: {
    TextHighlight
  },
  props: {
    areas: {
      type: Array,
      default() {
        return [];
      }
    },
    loading: {
       type: Boolean,
       default: false
    },
    searchText: {
      type: String,
      default: ''
    }    
  },
  data() {
    return {
      shownAreas: [],
      shownDirections: [],
      shownSkills: [],
      shownResults: [],
    };
  },
  computed:{
    filteredAreas(){
      return filter(this.areas, this.searchText.toLowerCase(), '');
    }
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
    toggleNode(shownNodes, nodeId){
      let index = shownNodes.indexOf(nodeId)
      if (index == -1){
        shownNodes.push(nodeId);
      } else {
        shownNodes.splice(index, 1);
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
    top: 90px
    z-index: 2
    border-bottom: 1px solid #e8e8e8
    padding-left: 95px

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

mark
  padding: 0 1px
</style>
