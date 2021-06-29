<template>
  <a-spin :spinning="loading">
    <div class="skills-activities">
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
        <div v-for="activity in activities" :key="activity.id" class="table-header__column table-header__column_activity">
          <div class="activity-circle" :style="{ 'background-color': activity.color }"></div>
          <div class="activity-name">{{activity.name}}</div>
        </div>
      </div>
      <div class="table-body" v-if="filteredAreas.length">
        <div class="table-row" v-for="area in filteredAreas" :key="area.id">
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
                    <div class="table-cell">{{[area.number, direction.number, skill.number].join('.')+'. '+skill.name}}</div>
                  </div>
                  <div v-for="activity in activities" :key="activity.id" class="table-row__column_activity">
                    <a-checkbox
                      :checked="!!handledActivities[activity.id].includes(skill.id)"
                      @change="setSkillLink($event, activity.id, skill.id)"
                    />
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
  </a-spin>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { Empty } from 'ant-design-vue';
export default {
  name: "AcitivitiesSkills",
  data() {
    return {
      loading: false,
    };
  },
  computed: {
    ...mapGetters({
      activities: "activities/getActivities",
      areasFetched: "skills/getFetched",
      filteredAreas: "skills/getFilteredAreas"
    }),
    handledActivities(){
      let res = {};
      for (let activity of this.activities)
        res[activity.id] = activity.skills;
      return res;
    }
  },
  async created(){
    if (!this.areasFetched)
    {
      this.loading = true;
      await this.fetchAreas();
      this.loading = false;
    }
  },
  methods: {
    ...mapActions({
      fetchAreas: "skills/fetchAreas",
      addLink: "activities/addLinkSkill",
      deleteLink: "activities/deleteLinkSkill",
    }),
    async setSkillLink(event, activityId, skillId){
      if (event.target.checked === true)
      {
        try {
          this.loading = true;
          let res = await this.addLink({activityId: activityId, skillId: skillId});
          if (res.status === 200) {
            this.$message.success("Успешно");
          } else {
            this.$message.error("Произошла ошибка");
          }
        } catch (e) {
          this.$message.error("Произошла ошибка");
        } finally {
          this.loading = false;
        }
      }
      else
      {
        try {
          this.loading = true;
          let res = await this.deleteLink({activityId: activityId, skillId: skillId});
          if (res.status === 200) {
            this.$message.success("Успешно");
          } else {
            this.$message.error("Произошла ошибка");
          }
        } catch (e) {
          this.$message.error("Произошла ошибка");
        } finally {
          this.loading = false;
        }
      }
    },
  },
  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },
};
</script>

<style lang="sass">
.skills-activities
  height: 100%
  overflow: auto

  .table-header
    display: flex
    height: 180px
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
    width: 15%

  .table-header__column_direction
    width: 17%
    border-left: 1px solid #e8e8e8

  .table-header__column_skill
    flex: 1
    border-left: 1px solid #e8e8e8

  .table-header__column_activity
    min-width: 50px
    max-width: 50px
    border-right: 1px solid #e8e8e8
    display: flex
    align-items: center
    writing-mode: vertical-lr
    transform: rotate(180deg)
    height: 100%
    padding: 5px

    .activity-circle
      width: 20px
      height: 20px
      border-radius: 10px
      margin-bottom: 10px

    .activity-name
      flex: 1

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
        z-index: 1
        top: 180px

    .table-row__container
      flex: 1
      display: flex
      flex-direction: column

    .table-row:first-child
      border-top: 0 none

    .table-row__column_area
      width: 15%

    .table-row__column_direction
      width: 20%
      border-left: 1px solid #e8e8e8

    .table-row__column_skill
      flex: 1
      border-left: 1px solid #e8e8e8

    .table-row__column_activity
      min-width: 50px
      max-width: 50px
      border-left: 1px solid #e8e8e8
      display: flex
      align-items: center
      justify-content: center

  .no-data
    padding: 50px 0
    border: 1px solid #e8e8e8
    border-top: 0 none
</style>
