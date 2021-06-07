<template>
  <div class="job-calendar">
    <div class="week">
      <div class="day" v-for="item, index in 7" :key="index">
        <div class="title">
          {{ daysOfWeek[index].long }}
        </div>
        <div class="job">
          <a-timeline>
            <template v-for="job in jobs">
              <a-timeline-item
                v-if="index === job.day"
                :color="job.activity.color"
                :key="job.id"
              >
                <div
                  class="job-card"
                  :style="{
                    'background-color': `${job.activity.color}4d`,
                    border: `1px solid ${job.activity.color}99`,
                  }"
                >
                  <div class="job-time">{{ formatTime(job.start_time) }}</div>
                  <a-dropdown
                    :trigger="['click']"
                    placement="bottomLeft"
                    class="dropdown--hover"
                  >
                    <a-icon class="icon-button" type="dash"></a-icon>
                    <a-menu slot="overlay">
                      <a-menu-item key="1" @click="openModalEdit(job)">
                        Изменить
                      </a-menu-item>
                      <a-menu-item
                        key="2"
                        @click="displayConfirmDelete(job, index)"
                      >
                        <span> Удалить </span>
                      </a-menu-item>
                    </a-menu>
                  </a-dropdown>
                  <div class="job-name">{{ job.activity.name }}</div>
                </div>
              </a-timeline-item>
            </template>
          </a-timeline>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import consts from "@/const";
import datetime from "@/mixins/datetime";
export default {
  name: "Template",
  mixins: [datetime],
  props: {
    jobs: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      daysOfWeek: consts.daysOfWeek,
    };
  },
  async created() {
  },
  methods: {

  },
  computed: {
  },
};
</script>

<style lang="sass">
.job-calendar
  overflow: auto
  flex: 1

  .week
    display: flex
    flex-direction: row
    min-height: 100%

    .day
      flex: 1 1 auto
      border-right: 1px solid #D9D9D9
      border-bottom: 1px solid #D9D9D9
      min-width: 150px
      max-width: 250px

      &:first-child
        border-left: 1px solid #D9D9D9

      .title
        text-align: center
        border-bottom: 1px solid #D9D9D9
        background-color: #1890ff
        padding: 10px
        color: #FFFFFF
        font-size: 1rem
        position: sticky
        top: 0
        z-index: 2

      .job
        padding: 15px 10px 10px 5px

        .job-card
          padding: 10px
          border-radius: 4px
          display: flex
          flex-wrap: wrap

          .job-time
            flex: 0 0 95%

          .dropdown--hover
            display: none
            max-width: 0
            height: 20px

            svg
              transform: rotate(90deg)
              margin-top: 3px

          &:hover
            .dropdown--hover
              display: unset

          .job-name
            flex: 0 0 100%
</style>
