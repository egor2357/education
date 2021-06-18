<template>
  <a-spin :spinning="loading">
    <div class="skill-development">

      <div class="top-bar">
        <div class="top-bar__side-block left"></div>
        <div class="title">Развитие навыков</div>
        <div class="top-bar__side-block right">
          <span class="date-range-label">Период:</span>
          <a-range-picker
            class="date-range-input"
            v-model="dateRange"
            @change="dateRangeChange"
            format="DD.MM.YYYY"
            :allowClear="false"
            separator="-"/>
        </div>
      </div>

      <div class="table-holder">
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
            <div class="table-cell">Количество обращений к навыку за период</div>
          </div>
        </div>
        <div class="table-body" v-if="areas.length">
          <div class="table-row" v-for="area in areas" :key="area.id">
            <div class="table-row__column table-row__column_area">
              <div class="table-cell">{{[area.number, area.name].join('. ')}}</div>
            </div>
            <div class="table-row__container">
              <div class="table-row" v-for="direction in area.development_directions" :key="direction.id">
                <div class="table-row__column table-row__column_direction">
                  <div class="table-cell">{{[area.number, direction.number].join('.')+'. '+direction.name}}</div>
                </div>
                <div class="table-row__container">
                  <div class="table-row" v-for="skill in direction.skills" :key="skill.id">
                    <div class="table-row__column_skill">
                      <div class="table-cell">
                        <span :class="{'skill-link' : reportsCountById[skill.id]}" @click="goToSkill(skill.id)">
                          {{[area.number, direction.number, skill.number].join('.')+'. '+skill.name}}
                        </span>
                      </div>
                    </div>
                    <div class="table-row__column_count">
                      <div class="table-cell">{{ skill.id in reportsCountById ? reportsCountById[skill.id] : 0 }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="no-data" v-else>
          <a-empty :image="simpleImage"/>
        </div>
      </div>
    </div>
  </a-spin>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { Empty } from 'ant-design-vue';
import moment from "moment";

export default {
  components: {
  },
  props: {
    dateRangeInit: {
      type: Array,
      default(){
        return [
          moment(new Date()).weekday(0),
          moment(new Date()).weekday(6)
        ];
      }
    },
  },
  name: "AllSkills",
  data() {
    return {
      loading: true,

      dateRange: this.dateRangeInit,

      reportsCountById: {},

    };
  },
  async created() {
    let fetches = []

    if (!this.areasFetched) {
      fetches.push(this.fetchAreas());
    }

    fetches.push(this.fetchSkillReports());

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;

  },
  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },
  methods: {
    ...mapActions({
      fetchAreas: "skills/fetchAreas",
    }),

    setReportsCountById(reports){
      this.reportsCountById = {};
      for (let report of reports) {
        if (report.skill_id in this.reportsCountById) {
          this.reportsCountById[report.skill_id] += 1;
        } else {
          this.reportsCountById[report.skill_id] = 1;
        }
      }
    },
    async fetchSkillReports(){
      try {
        this.loading = true;
        let firstQParameter = `date_from=${this.dateRange[0].format("YYYY-MM-DD")}`;
        let secondQParameter = `date_to=${this.dateRange[1].format("YYYY-MM-DD")}`;
        let thirdQParameter = `is_affected=true`;
        let QParameters = `?${firstQParameter}&${secondQParameter}&${thirdQParameter}`;
        let res = await this.$axios.get(`/api/skill_reports/${QParameters}`);
        if (res.status === 200) {
          this.setReportsCountById(res.data);
        } else {
          this.$message.error("Произошла ошибка при загрузке отчетов");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка при загрузке отчетов");
      } finally {
        this.loading = false;
      }
    },
    goToSkill(skillId){
      if (this.reportsCountById[skillId]) {
        this.$router.push({name: "SkillDetails", params: {id: skillId}})
      }
    },
    dateRangeChange(value){
      this.$emit("changeRange", value);
      this.fetchSkillReports();
    },
  },
  computed: {
    ...mapGetters({
      areasFetched: "skills/getFetched",
      areas: "skills/getFilteredAreas",
    }),
  },

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
      width: 200px

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
    z-index: 2
    position: sticky
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
    min-width: 150px
    max-width: 150px
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
        flex: 1

    .table-row__column
      .table-cell
        position: sticky
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
      min-width: 150px
      max-width: 150px
      border-left: 1px solid #e8e8e8
      display: flex
      align-items: center
      justify-content: center

    .skill-link
      color: #1890ff
      cursor: pointer
      transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);

    .skill-link:hover
      color: #40a9ff

  .no-data
    padding: 50px 0
    border: 1px solid #e8e8e8
    border-top: 0 none

</style>
