<template>
  <a-spin :spinning="loading">
    <div class="skill-development">
      <div class="top-bar">
        <div class="top-bar__side-block left">
          <a-checkbox v-model="doNotShowNotCalled" @change="changeShowCalled">
            Скрыть незатронутые навыки
          </a-checkbox>
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

      <div id="table" class="table-holder">
        <div>
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
            <div class="table-header__column table-header__column_count">
              <div class="table-cell">
                Количество обращений к навыку за период
              </div>
            </div>
            <div class="table-header__column table-header__column_mark">
              <div class="table-cell">
                Оценка освоения навыка
              </div>
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
                          <span
                            :class="{
                              'skill-link': reportsStatisticsById[skill.id]
                            }"
                            @click="goToSkill(skill.id)"
                          >
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
                        </div>
                      </div>
                      <div class="table-row__column_count">
                        <div class="table-cell">
                          {{
                            skill.id in reportsStatisticsById
                              ? reportsStatisticsById[skill.id].called
                              : 0
                          }}
                          /
                          {{
                            skill.id in reportsStatisticsById
                              ? reportsStatisticsById[skill.id].planned
                              : 0
                          }}
                        </div>
                      </div>
                      <div class="table-row__column_mark">
                        <div class="table-cell">
                          {{
                            skill.id in reportsStatisticsById
                              ? reportsStatisticsById[skill.id].value
                              : "-"
                          }}
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
      doNotShowNotCalled: false,

      reportsStatisticsById: {}
    };
  },

  computed: {
    ...mapGetters({
      areasFetched: "skills/getFetched",
      areas: "skills/getFilteredAreas",
      scrollPosition: "skills/getScrollPosition"
    }),
    filteredAreas() {
      if (!this.doNotShowNotCalled) {
        return this.areas;
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
                  skills: dir.skills.filter(
                    skill => String(skill.id) in this.reportsStatisticsById
                  )
                };
              })
              .filter(direction => direction.skills.length)
          };
        })
        .filter(area => area.development_directions.length);
    }
  },

  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },

  async created() {
    let fetches = [];

    if (!this.areasFetched) {
      fetches.push(this.fetchAreas());
    }

    if (this.$route.query.showCalled) {
      this.doNotShowNotCalled = this.$route.query.showCalled === "true";
    }

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;

    if (!this.setDateRange(this.$route)) {
      this.dateRangeChange(this.dateRange, true);
      return;
    }

    this.fetchSkillReportsStatistics();
  },

  beforeRouteUpdate(to, from, next) {
    if (!this.setDateRange(to)) {
      this.dateRangeChange(this.dateRange, true);
      return;
    }
    this.fetchSkillReportsStatistics();
    next();
  },

  updated() {
    const table = document.getElementById("table");
    if (table) {
      if (this.scrollPosition) {
        table.scrollTop = this.scrollPosition;
      }
      table.addEventListener("scroll", this.saveScrollPosition);
    }
  },

  beforeDestroy() {
    const table = document.getElementById("table");
    if (table) {
      table.removeEventListener("scroll", this.saveScrollPosition);
    }
  },

  methods: {
    ...mapActions({
      fetchAreas: "skills/fetchAreas"
    }),
    ...mapMutations({
      setScrollPosition: "skills/setScrollPosition"
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
          `/api/skill_reports/statistics/${QParameters}`
        );
        if (res.status === 200) {
          this.reportsStatisticsById = res.data;
        } else {
          this.$message.error("Произошла ошибка при загрузке отчетов");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка при загрузке отчетов");
      } finally {
        this.loading = false;
      }
    },
    goToSkill(skillId) {
      if (this.reportsStatisticsById[skillId]) {
        this.$router.push({
          name: "SkillDetails",
          params: { id: skillId },
          query: {
            dateFrom: this.$route.query.dateFrom,
            dateTo: this.$route.query.dateTo,
            showCalled: this.$route.query.showCalled
          }
        });
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
        showCalled: this.doNotShowNotCalled
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

    changeShowCalled(event) {
      if (this.$route.query.showCalled != event.target.checked) {
        this.$router.replace({
          name: this.$route.name,
          query: { ...this.$route.query, showCalled: event.target.checked }
        });
      }
    },

    saveScrollPosition(e) {
      this.setScrollPosition(e.target.scrollTop);
    }
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

  .table-holder
    flex: 1
    overflow: auto

  .table-header
    display: flex
    height: 60px
    align-items: center
    background: #fafafa
    border: 1px solid #e8e8e8
    overflow: hidden
    line-height: 15px
    z-index: 3
    position: sticky
    position: -webkit-sticky
    top: 0

  .table-header__column
    overflow: hidden
    display: flex
    align-items: center
    height: 100%

  .table-header__column_area
    width: 20%

  .table-header__column_direction
    width: 20%
    border-left: 1px solid #e8e8e8

  .table-header__column_skill
    flex: 1
    border-left: 1px solid #e8e8e8

  .table-header__column_count
    width: 160px
    border-left: 1px solid #e8e8e8
    display: flex
    align-items: center

  .table-header__column_mark
    width: 160px
    border-left: 1px solid #e8e8e8
    display: flex
    align-items: center

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
        flex: 1 1 auto

    .table-row__column
      .table-cell
        position: sticky
        position: -webkit-sticky
        z-index: 1
        top: 60px

    .table-row__container
      flex: 1
      display: flex
      flex-direction: column

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

    .table-row__column_count
      width: 160px
      border-left: 1px solid #e8e8e8
      display: flex
      align-items: center
      justify-content: center

    .table-row__column_mark
      width: 160px
      border-left: 1px solid #e8e8e8
      display: flex
      align-items: center
      justify-content: center

    .skill-link
      color: #1890ff
      cursor: pointer
      transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1)

    .skill-link:hover
      color: #40a9ff

  .no-data
    padding: 50px 0
    border: 1px solid #e8e8e8
    border-top: 0 none
</style>
