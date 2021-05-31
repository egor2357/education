<template>
  <div class="table-presence-activity">
    <a-table
      :pagination="false"
      size="middle"
      :loading="loading || loadingMain"
      :data-source="data"
      :columns="columns"
      :scroll="{ y: 'calc(100vh - 320px)', x: 'auto' }"
    >
      <span slot="activityTitle">
        <span>Виды деятельности</span>
        <a-icon
          @click="$emit('close')"
          class="icon-button"
          type="swap"
          style="padding-left: 10px"
        />
      </span>
      <template slot="day" slot-scope="text, record">
        <a-dropdown
          :trigger="['click']"
          placement="bottomLeft"
          v-if="text"
          :disabled="text.value === null"
        >
          <div
            :class="[
              text.value === true
                ? 'available'
                : text.value === false
                ? 'not-available'
                : 'empty',
              { 'left-border': text.leftBorder },
              { 'right-border': text.rightBorder },
              { 'no-date': !text.displayDate },
            ]"
          >
            <div v-if="text.displayDate" style="color: #fff">
              {{ text.day }}
            </div>
          </div>
          <a-menu slot="overlay">
            <a-menu-item key="1" @click="$emit('displayEdit', text)">
              Изменить
            </a-menu-item>
            <a-menu-item key="2" @click="$emit('deleteConfirm', text, record)">
              <span> Удалить </span>
            </a-menu-item>
          </a-menu>
        </a-dropdown>
      </template>
    </a-table>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import common from "@/mixins/common";
import moment from "moment";
export default {
  name: "TableActivities",
  mixins: [common],
  props: {
    daysOfMonth: {
      type: Array,
      default: () => [],
    },
    specialists: {
      type: Array,
      default: () => [],
    },
    presences: {
      type: Array,
      default: () => [],
    },
    month: {
      type: Object,
    },
    year: {
      type: Number,
    },
    needUpdate: {
      type: Boolean,
      default: false,
    },
    loadingMain: {
      type: Boolean,
    },
  },
  data() {
    return {
      data: [],
      loading: true,
      activitiesSpecialists: {},
      columnsStart: [
        {
          dataIndex: "activity",
          customRender: (text) => {
            if (!text.empty) {
              return {
                children: (
                  <div class="activities">
                    <div
                      class="activity-block"
                      style={`background-color:${text.color}4d; border: 1px solid ${text.color}99; `}
                    >
                      {text.name}
                    </div>
                  </div>
                ),
                attrs: {
                  rowSpan: text.length,
                },
              };
            } else {
              return {
                attrs: {
                  rowSpan: 0,
                },
              };
            }
          },
          width: "170px",
          slots: {
            title: "activityTitle",
          },
        },
        {
          title: "Специалист",
          key: "specialist",
          width: "150px",
          customRender: (text) => {
            if (text.specialist) {
              return this.formatSpecialist(text.specialist);
            } else {
              return null;
            }
          },
        },
      ],
      columns: [],
    };
  },
  async created() {
    this.loading = true;
    await this.prepareColumns();
    await this.prepareData();
    this.loading = false;
  },
  methods: {
    prepareColumns() {
      this.columns = this.columnsStart.slice();
      for (let day of this.daysOfMonth) {
        this.columns.push({
          title: day.num,
          dataIndex: day.num,
          scopedSlots: {
            customRender: "day",
          },
          align: "center",
          class: [{ weekend: day.weekend }, "day"],
        });
      }
    },
    prepareData() {
      this.data = [];
      let indexRow = 0;
      let currentDay = null;
      let value = null;
      let dateFrom = null;
      let dateTo = null;
      let displayDate = false;
      let leftBorder = false;
      let rightBorder = false;
      let presenceData = null;
      let indexActivity = null;
      for (let activity of this.activities) {
        this.data.push({
          key: `${activity.id}`,
          activity: {
            empty: false,
            length: 1,
            name: activity.name,
            color: activity.color,
          },
        });
        indexActivity = this.data.length - 1;
        indexRow = indexActivity;
        for (let specialist of this.specialists) {
          if (specialist.user && specialist.user.is_staff === false) {
            for (let specActivity of specialist.activities) {
              if (specActivity.activity.id === activity.id) {
                if (this.data[indexActivity].specialist) {
                  this.data[indexActivity].activity.length += 1;
                  this.data.push({
                    key: `${activity.id}_${specialist.id}`,
                    activity: {
                      empty: true,
                    },
                    specialist: specialist,
                  });
                  indexRow += 1;
                } else {
                  this.data[indexRow].key = `${activity.id}_${specialist.id}`;
                  this.data[indexRow].specialist = specialist;
                }
                for (let day of this.daysOfMonth) {
                  value = null;
                  displayDate = false;
                  leftBorder = false;
                  rightBorder = false;
                  presenceData = null;
                  currentDay = moment(
                    `${this.year}-${this.month.value + 1}-${day.num}`,
                    "YYYY-MM-DD"
                  );
                  for (let presence of this.presences) {
                    dateFrom = null;
                    dateTo = null;
                    if (presence.specialist_id === specialist.id) {
                      dateFrom = moment(presence.date_from);
                      dateTo = moment(presence.date_to);
                      if (currentDay.isBetween(dateFrom, dateTo, "day", [])) {
                        value = presence.is_available;
                        presenceData = presence;
                        if (dateFrom.date() === 1 && currentDay.date() === 1) {
                          leftBorder = true;
                          displayDate = true;
                        }
                        if (
                          dateTo.date() === this.lastDay &&
                          currentDay.date() === this.lastDay
                        ) {
                          rightBorder = true;
                          displayDate = true;
                        }
                        break;
                      }
                    }
                  }
                  this.data[indexRow][day.num] = {
                    value: value,
                    leftBorder: leftBorder,
                    rightBorder: rightBorder,
                    displayDate: displayDate,
                    presence: presenceData,
                    day: day.num,
                  };
                }
                for (let filledDay of this.daysOfMonth) {
                  if (this.data[indexRow][filledDay.num].value !== null) {
                    if (
                      this.data[indexRow][filledDay.num - 1] &&
                      (this.data[indexRow][filledDay.num - 1].value === null ||
                        (this.data[indexRow][filledDay.num - 1].value !==
                          null &&
                          this.data[indexRow][filledDay.num].presence.id !==
                            this.data[indexRow][filledDay.num - 1].presence
                              .id &&
                          this.data[indexRow][filledDay.num].presence.id !==
                            this.data[indexRow][filledDay.num - 1].presence
                              .main_interval_id))
                    ) {
                      this.data[indexRow][filledDay.num].leftBorder = true;
                      this.data[indexRow][filledDay.num].displayDate = true;
                    }
                    if (
                      this.data[indexRow][filledDay.num + 1] &&
                      (this.data[indexRow][filledDay.num + 1].value === null ||
                        (this.data[indexRow][filledDay.num + 1].value !==
                          null &&
                          this.data[indexRow][filledDay.num].presence.id !==
                            this.data[indexRow][filledDay.num + 1].presence.id))
                    ) {
                      this.data[indexRow][filledDay.num].rightBorder = true;
                      this.data[indexRow][filledDay.num].displayDate = true;
                    }
                    if (
                      this.data[indexRow][filledDay.num + 1] &&
                      this.data[indexRow][filledDay.num].value === false &&
                      this.data[indexRow][filledDay.num + 1].value === true
                    ) {
                      this.data[indexRow][filledDay.num].rightBorder = false;
                      this.data[indexRow][filledDay.num].displayDate = true;
                      this.data[indexRow][filledDay.num + 1].displayDate = true;
                    }
                  }
                }
                break;
              }
            }
          }
        }
      }
    },
    async updateData() {
      this.loading = true;
      setTimeout(async () => {
        await this.prepareColumns();
        await this.prepareData();
        this.loading = false;
      }, 1)
    },
  },
  computed: {
    ...mapGetters({
      activities: "activities/getActivities",
    }),
  },
  watch: {
    async needUpdate(value) {
      if (value === true) {
        await this.updateData();
        this.$emit('updated');
      }
    },
  },
};
</script>

<style lang="sass">
.table-presence-activity
  flex: 1
  overflow: auto
  td[rowspan]
    background-color: unset !important
  .activities
    display: flex
    flex-wrap: wrap
    .activity-block
      padding: 3px
      border-radius: 4px
  /*.day*/
    /*padding: 0 !important*/
    /*min-width: 30px*/
    /*.not-available, .available, .empty*/
      /*width: 100%*/
      /*display: inline-block*/
      /*height: 10px*/
      /*margin-top: 5px*/
      /*&:empty::before*/
        /*content: "\A0"*/
      /*&.no-date*/
        /*margin-top: 20px*/
    /*.not-available*/
      /*border-bottom: 2px solid #FFA756*/
    /*.available*/
      /*border-bottom: 2px solid #3DC5FF*/
    /*.left-border*/
      /*border-top-left-radius: 0*/
      /*border-bottom-left-radius: 0*/
      /*&.not-available*/
        /*border-left: 2px solid #FFA756*/
      /*&.available*/
        /*border-left: 2px solid #3DC5FF*/
    /*.right-border*/
      /*border-top-right-radius: 0*/
      /*border-bottom-right-radius: 0*/
      /*&.not-available*/
        /*border-right: 2px solid #FFA756*/
      /*&.available*/
        /*border-right: 2px solid #3DC5FF*/
</style>
