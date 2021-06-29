<template>
  <div class="presence-chart">
    <div class="presence-chart__table">
      <div class="presence-chart__table-header">
        <div
          class="presence-chart__table-header-specialist-cell"
          v-if="!specReadOnly"
        >
          Специалист
        </div>
        <div
          class="presence-chart__table-header-day-cell"
          v-for="day of tableData.daysInMonth"
          :key="day.num"
          :class="{ weekend: day.weekend }"
        >
          {{ day.num }}
        </div>
      </div>
      <div class="presence-chart__table-body">
        <div
          class="presence-chart__table-body-row"
          v-for="row in tableData.specialists"
          :key="row.id"
        >
          <div
            class="presence-chart__table-body-specialist-cell"
            v-if="!specReadOnly"
          >
            <Popover :data="{ name: row.fullName, specialist: row }" />
          </div>
          <div class="presence-chart__table-body-chart-holder">
            <div
              class="presence-interval"
              v-for="interval in row.presence"
              :key="interval.id"
              :class="{ start: interval.hasStart, end: interval.hasEnd }"
              :style="{
                width:
                  (interval.daysCount * 100) / tableData.daysInMonth.length +
                  '%',
                left:
                  ((interval.dayFrom - 1) * 100) /
                    tableData.daysInMonth.length +
                  '%',
              }"
            >
              <a-dropdown
                v-for="(date, index) in interval.daysCount"
                :key="index"
                :trigger="['click']"
                placement="bottomLeft"
              >
                <div
                  class="presence-interval-day"
                  :class="{
                    quarantine: date <= interval.quarantineDaysCount,
                    available: date > interval.quarantineDaysCount,
                  }"
                >
                  {{
                    interval.labledDays.includes(date)
                      ? date + interval.dayFrom - 1
                      : ""
                  }}
                </div>
                <a-menu slot="overlay" v-if="!specReadOnly">
                  <a-menu-item
                    key="1"
                    @click="
                      $emit('displayEdit', { presence: interval.editableData })
                    "
                  >
                    Изменить
                  </a-menu-item>
                  <a-menu-item
                    key="2"
                    @click="
                      $emit('displayDeleteConfirm', {
                        specialist: row.fullName,
                        presence: interval.editableData,
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
    </div>
  </div>
</template>
<script>
import moment from "moment";
import Popover from "@/components/AvailableChart/Popover";
export default {
  name: "PresenceChart",
  components: { Popover },
  props: {
    tableData: {
      type: Object,
      default() {
        return {
          daysInMonth: [],
          specialists: [],
        };
      },
    },
    daysInMonth: {
      type: Array,
      default() {
        return [];
      },
    },
    specReadOnly: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
<style lang="sass">
.presence-chart
  flex: 1
  overflow: hidden
  display: flex
  flex-direction: column
  max-width: 1650px
  margin: 0 auto
  min-width: 870px

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
    position: -webkit-sticky
    top: 0
    cursor: default
    z-index: 1

  &__table-header-specialist-cell
    width: 250px
    padding: 5px 10px

  &__table-header-day-cell
    min-width: 20px
    max-width: 55px
    flex: 1
    text-align: center
    padding: 7px 0
    font-size: 16px

    &.weekend
      color: #e55
      font-weight: bold

  &__table-body
    flex: 1

  &__table-body-row
    line-height: 34px
    display: flex
    border-bottom: 1px solid #e8e8e8
    align-items: center
    transition: background .3s

  &__table-body-row:hover
    background: #e6f7ff

  &__table-body-specialist-cell
    width: 250px
    padding: 5px 10px
    cursor: default

  &__table-body-chart-holder
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
        background: #cfcfcf

      &.available
        background: #3DC5FF

  &__table-body-day-cell
    flex: 1
    min-width: 20px
    max-width: 50px
    height: 30px
    color: #fff
    text-align: center
    line-height: 30px

    .cell-trigger
      height: 100%

    &.chart
      background: #FFA756
      cursor: pointer

    &.start
      border-top-left-radius: 4px
      border-bottom-left-radius: 4px

    &.available
      background: #3DC5FF
</style>
