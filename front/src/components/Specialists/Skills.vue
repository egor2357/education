<template>
  <a-spin :spinning="loading">
    <div class="specialist-skills">
      <div class="table-header">
        <div class="table-header__column table-header__column_area">
          <div class="table-cell">Образовательная область</div>
        </div>
        <div class="table-header__column table-header__column_direction">
          <div class="table-cell">Направление развития</div>
        </div>
        <div class="table-header__column table-header__column_skill">
          <div class="table-cell">Навык</div>
        </div>
        <div class="table-header__column table-header__column_coefficient">
          <div class="table-cell">Коэффициент развития</div>
        </div>
      </div>
      <div class="table-body" v-if="filteredAreas.length">
        <div class="table-row" v-for="area in filteredAreas" :key="area.id">
          <div class="table-row__column table-row__column_area">
            <div class="table-cell">
              {{ [area.number, area.name].join(". ") }}
            </div>
          </div>
          <div class="table-row__container">
            <div
              class="table-row"
              v-for="direction in area.development_directions"
              :key="direction.id"
            >
              <div class="table-row__column table-row__column_direction">
                <div class="table-cell">
                  {{
                    [area.number, direction.number].join(".") +
                    ". " +
                    direction.name
                  }}
                </div>
              </div>
              <div class="table-row__container">
                <div
                  class="table-row"
                  v-for="skill in direction.skills"
                  :key="skill.id"
                >
                  <div class="table-row__column_skill">
                    <div class="table-cell">
                      {{
                        [area.number, direction.number, skill.number].join(
                          "."
                        ) +
                        ". " +
                        skill.name
                      }}
                    </div>
                  </div>
                  <div class="table-row__column_coefficient">
                    <div class="table-cell">
                      <a-checkbox
                        v-if="skillsData[skill.id]"
                        :checked="!!skillsData[skill.id].linkId"
                        @change="setSkillState($event, skill.id)"
                      />
                      <a-input-number
                        class="skill-coefficient"
                        v-if="skillsData[skill.id]"
                        :step="0.1"
                        :min="0"
                        :max="1"
                        :disabled="!skillsData[skill.id].linkId"
                        v-model="skillsData[skill.id].coefficient"
                        @blur="
                          setSkillCoefficient(
                            $event,
                            skillsData[skill.id].linkId
                          )
                        "
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="no-data" v-else>
        <a-empty :image="simpleImage" />
      </div>
    </div>
  </a-spin>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { Empty } from "ant-design-vue";
export default {
  name: "Skills",
  data() {
    return {
      loading: false,
      skillsData: {},
    };
  },
  props: {
    specialistSkills: {
      type: Array,
    },
    specialistId: {
      type: [Number, String],
    },
  },
  computed: {
    ...mapGetters({
      areas: "skills/getAreas",
      areasFetched: "skills/getFetched",
      filteredAreas: "skills/getFilteredAreas",
    }),
  },
  async created() {
    if (!this.areasFetched) {
      this.loading = true;
      await this.fetchAreas();
      this.loading = false;
    }
    this.makeSkillsData();
  },
  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },
  methods: {
    ...mapActions({
      fetchAreas: "skills/fetchAreas",
      addSkill: "specialists/addSpecialistSkill",
      editSkill: "specialists/editSpecialistSkill",
      deleteSkill: "specialists/deleteSpecialistSkill",
    }),
    makeSkillsData() {
      this.skillsData = {};
      this.coefficients = [];
      let index = 0;
      for (let area of this.areas) {
        for (let direction of area.development_directions) {
          for (let skill of direction.skills) {
            this.$set(this.skillsData, skill.id, {
              linkId: null,
              coefficient: null,
            });
          }
        }
      }
      for (let skill of this.specialistSkills) {
        this.skillsData[skill.skill.id].linkId = skill.id;
        this.skillsData[skill.skill.id].coefficient = skill.coefficient;
      }
    },
    async setSkillState(event, skillId) {
      this.loading = true;
      if (event.target.checked === true) {
        let res = await this.addSkill({
          skill_id: skillId,
          specialist_id: this.specialistId,
          coefficient: 1,
        });
        if (res.status === 201) {
          this.makeSkillsData();
          this.$message.success("Навык у специалиста успешно добавлен");
        } else {
          this.$message.error("Произошла ошибка");
        }
      } else {
        let res = await this.deleteSkill({
          linkId: this.skillsData[skillId].linkId,
          specialistId: this.specialistId,
        });
        if (res.status === 204) {
          this.makeSkillsData();
          this.$message.success("Навык у специалиста успешно удалён");
        } else {
          this.$message.error("Произошла ошибка");
        }
      }
      this.loading = false;
    },
    async setSkillCoefficient(event, linkId) {
      this.loading = true;
      let res = await this.editSkill({
        linkId: linkId,
        coefficient: Number(event.target.value),
        specialistId: this.specialistId,
      });
      this.loading = false;
      if (res.status === 200) {
        this.makeSkillsData();
        this.$message.success("Коэффициент успешно изменён");
      } else {
        this.$message.error("Произошла ошибка");
      }
    },
  },
};
</script>

<style lang="sass">
.specialist-skills
  height: 100%
  overflow: auto

  .table-header
    display: flex
    height: 50px
    align-items: center
    background: #fafafa
    border: 1px solid #e8e8e8
    overflow: hidden
    line-height: 15px
    z-index: 2
    position: sticky
    position: -webkit-sticky
    top: 0

  .table-header__column
    overflow: hidden

  .table-header__column_area
    width: 20%

  .table-header__column_direction
    width: 20%
    border-left: 1px solid #e8e8e8

  .table-header__column_skill
    flex: 1
    border-left: 1px solid #e8e8e8

  .table-header__column_coefficient
    width: 130px
    border-left: 1px solid #e8e8e8

  .table-cell
    padding: 10px 15px
    display: flex
    align-items: center
    min-height: 52px
    word-break: break-word

  .table-body
    border: 1px solid #e8e8e8
    border-top: 0 none

    .table-row
      border-top: 1px solid #e8e8e8
      display: flex

    .table-row__column
      .table-cell
        position: sticky
        position: -webkit-sticky
        z-index: 1
        top: 50px

    .table-row__container
      flex: 1

    .table-row:first-child
      border-top: 0 none

    .table-row__column_area
      width: 20%

    .table-row__column_direction
      width: 25%
      border-left: 1px solid #e8e8e8

    .table-row__column_skill
      flex: 1
      border-left: 1px solid #e8e8e8

    .table-row__column_coefficient
      width: 130px
      border-left: 1px solid #e8e8e8

    .skill-coefficient
      width: 60px
      margin-left: 10px

  .no-data
    padding: 50px 0
    border: 1px solid #e8e8e8
    border-top: 0 none
</style>
