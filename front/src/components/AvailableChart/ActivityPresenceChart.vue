<template>
  <div class="activity-presence-chart">
    <div class="activity-presence-chart__table">
      <div class="activity-presence-chart__table-header">
        <div class="activity-presence-chart__table-header-activity-cell">Вид деятельности</div>
        <div class="activity-presence-chart__table-header-specialist-cell">Специалист</div>
        <div class="activity-presence-chart__table-header-day-cell" v-for="day of daysInMonth" :key="day.num" :class="{weekend: day.weekend}">{{day.num}}</div>
      </div>
      <div class="activity-presence-chart__table-body">
        <div class="activity-presence-chart__activity-row" v-for="activity in mainData" :key="activity.id">
          <div class="activity-presence-chart__activity-cell">
            <div
              class="activity-presence-chart__activity-block"
              :style="{'background-color': activity.color+'4d', border: '1px solid '+activity.color+'99'}">{{activity.name}}</div>
          </div>
          <div class="activity-presence-chart__specialist-presence-container">
            <div class="activity-presence-chart__specialist-presence-row" v-for="specialist in activity.specialists" :key="specialist.id">
              <div class="activity-presence-chart__specialist-cell">{{specialist.fullName}}</div>
              <div class="activity-presence-chart__specialist-chart-holder">
                <div class="presence-interval"
                  v-for="interval in specialist.presence"
                  :key="interval.id"
                  :class="{start: interval.hasStart, end: interval.hasEnd}"
                  :style="{
                            width: interval.daysCount*100/daysInMonth.length+'%',
                            left: (interval.dayFrom-1)*100/daysInMonth.length+'%'
                          }"
                >
                  <a-dropdown v-for="date, index in interval.daysCount" :key="index"
                    :trigger="['click']"
                    placement="bottomLeft"
                  >
                    <div class="presence-interval-day"
                      :class="{quarantine: date <= interval.quarantineDaysCount, available: date > interval.quarantineDaysCount}"
                    >
                      {{interval.labledDays.includes(date) ? date+interval.dayFrom-1 : ''}}
                    </div>
                    <a-menu slot="overlay">
                      <a-menu-item key="1" @click="$emit('displayEdit', {presence: interval.editableData})">
                        Изменить
                      </a-menu-item>
                      <a-menu-item key="2" @click="$emit('displayDeleteConfirm', {specialist: specialist.fullName, presence: interval.editableData})">
                        <span> Удалить </span>
                      </a-menu-item>
                    </a-menu>
                  </a-dropdown>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import moment from "moment";
  export default {
    name: "ActivityPresenceChart",
    props: {
      tableData: {
        type: Object,
        default(){
          return {
            specialists: []
          };
        }
      },
      daysInMonth: {
        type: Array,
        default(){
          return []
        }
      },
      activities: {
        type: Array,
        default(){
          return []
        }
      }
    },
    computed: {
      mainData(){
        let result = this.activities.map((activity) => {return {id: activity.id, color: activity.color, name: activity.name, specialists: []}});
        this.tableData.specialists.forEach(specialist => {
          specialist.activities.forEach(specialistActivity => {
            let activityItem = result.find(item => item.id == specialistActivity.activity.id);
            if (activityItem)
              activityItem.specialists.push({id: specialist.id, fullName: specialist.fullName, presence: specialist.presence});
          })
        })
        return result;
      }
    }
  }
</script>
<style lang="sass">
  .activity-presence-chart
    flex: 1
    overflow: hidden
    display: flex
    flex-direction: column
    max-width: 1650px
    margin: 0 auto
    min-width: 990px

    &__table
      flex: 1
      overflow: auto
      display: flex
      flex-direction: column

    &__table-header
      display: flex
      line-height: 34px
      border-bottom: 1px solid #e8e8e8
      background: #fafafa
      position: sticky
      top: 0
      cursor: default
      z-index: 1

    &__table-header-activity-cell
      width: 170px
      padding: 5px 10px

    &__table-header-specialist-cell
      width: 200px
      padding: 5px 10px

    &__table-header-day-cell
      min-width: 20px
      max-width: 50px
      flex: 1
      text-align: center
      padding: 7px 0;
      font-size: 16px

      &.weekend
        color: #e55
        font-weight: bold

    &__table-body
      flex: 1

    &__activity-row
      line-height: 34px
      display: flex
      border-bottom: 1px solid #e8e8e8
      align-items: center

    &__activity-cell
      width: 170px
      display: flex

    &__activity-block
      padding: 3px
      border-radius: 4px
      line-height: 24px
      margin: 5px
      box-shadow: 0 0 3px 1px #eee

    &__specialist-presence-container
      flex: 1
      display: flex
      flex-direction: column

    &__specialist-presence-row
      display: flex
      align-items: center
      border-bottom: 1px solid #e8e8e8

      &:last-child
        border-bottom: 0 none

    &__specialist-presence-row:hover
      background: #def

    &__specialist-cell
      width: 200px
      padding: 5px 10px
      cursor: default

    &__specialist-chart-holder
      display: flex
      flex: 1
      position: relative
      height: 30px

      .presence-interval
        display: flex
        position: absolute
        box-shadow: 0 1px 3px 1px #dedede
        top: 0
        overflow: hidden
        height: 30px
        line-height: 30px
        cursor: pointer

        &.start
          border-top-left-radius: 4px
          border-bottom-left-radius: 4px

        &.end
          border-top-right-radius: 4px
          border-bottom-right-radius: 4px

      .presence-interval-day
        text-align: center
        flex: 1
        color: #fff

        &.quarantine
          background: #FFA756

        &.available
          background: #3DC5FF

      &.start
        border-top-left-radius: 4px
        border-bottom-left-radius: 4px

      &.available
        background: #3DC5FF
</style>