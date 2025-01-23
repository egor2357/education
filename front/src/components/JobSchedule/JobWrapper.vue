<template>
  <ScheduleReadOnly v-if="!userInfo.staff" />
  <JobSchedule v-else />
</template>

<script>
import { mapGetters } from "vuex";
import ScheduleReadOnly from "@/components/JobSchedule/ScheduleReadOnly";
import JobSchedule from "@/components/JobSchedule/JobSchedule";
export default {
  components: {
    ScheduleReadOnly,
    JobSchedule,
  },
  name: "JobWrapper",
  computed: {
    ...mapGetters({
      userInfo: "auth/getUserInfo",
    }),
  },
};
</script>

<style lang="sass">
.job-schedule
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

  .job-schedule__interval
    display: flex
    justify-content: center
    font-size: 20px
    align-items: center
    margin-bottom: 10px

    &--small
      font-size: 18px

  .job-schedule__interval-label
    min-width: 300px
    text-align: center

  &__calendar
    overflow: auto
    flex: 1

    &__week
      display: flex
      flex-direction: row
      min-height: 100%

    &__date
      flex: 1 1 auto
      border-right: 1px solid #D9D9D9
      border-bottom: 1px solid #D9D9D9
      min-width: 150px
      max-width: 250px

      &:first-child
        border-left: 1px solid #D9D9D9

      &-title
        text-align: center
        border-bottom: 1px solid #D9D9D9
        border-top: 1px solid #D9D9D9
        background-color: #f4f4f4
        font-size: 1rem
        position: sticky
        position: -webkit-sticky
        top: 0
        z-index: 3
        display: flex
        flex-direction: row
        align-items: center
        padding: 5px 10px
        &-day
          font-size: 18px
          margin-right: 10px
          flex: 1
        &-weekday
          font-size: 34px
          font-weight: bold
          text-align: center
        &.weekend
          .job-schedule__calendar__date-title-weekday
            color: #f55

    &__jobs
      padding: 15px 10px 10px 5px

    &__template
      padding: 5px 10px
      border-radius: 4px
      display: flex
      flex-wrap: wrap
      background-color: #f9f9f9
      border: 1px solid #cccccc
      position: relative
      &-time
        flex: 0 0 95%
        color: #999
      &-activity-name
        color: #999
      &:hover &-overlay
        display: flex
      &-overlay
        display: none
        position: absolute
        top: 0
        border-radius: 4px
        left: 0
        width: 100%
        height: 100%
        justify-content: center
        align-items: center
        background-color: #ffffffc2
        &__button

  &__switcher
    margin-top: 10px
</style>
