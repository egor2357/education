<template>
  <div class="available-table">
    <div class="title-month">
      <a-icon class="icon-button" type="left" @click="changeMonth(false)" />
      <span class="text">{{ month.name }} {{ year }}</span>
      <a-icon class="icon-button" type="right" @click="changeMonth(true)" />
    </div>
    <a-table
      :data-source="data"
      :pagination="false"
      size="middle"
      :loading="loading"
    >
      <a-table-column
        key="name"
        title="Специалист"
        data-index="name"
        fixed="left"
      >
        <template slot-scope="text, record">
          <Popover :data="record" />
        </template>
      </a-table-column>
      <a-table-column
        v-for="day in daysOfMonth"
        :key="day.num"
        class="day"
        align="center"
        :data-index="day.num"
        :class="day.weekend ? 'weekend' : ''"
      >
        <span slot="title">{{ day.num }}</span>
        <template slot-scope="text, record">
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
              ]"
            >
              <div v-if="text.displayDate" style="color: #fff">
                {{ day.num }}
              </div>
            </div>
            <a-menu slot="overlay">
              <a-menu-item key="1" @click="$emit('displayEdit', text)">
                Изменить
              </a-menu-item>
              <a-menu-item key="2" @click="displayDeleteConfirm(text, record)">
                <span> Удалить </span>
              </a-menu-item>
            </a-menu>
          </a-dropdown>
        </template>
      </a-table-column>
    </a-table>
  </div>
</template>
<script>
import moment from "moment";
import { mapGetters, mapActions } from "vuex";
import Popover from "@/components/AvailableChart/Popover";
export default {
  name: "Table",
  components: {Popover},
  data() {
    return {
      data: [],
      daysOfMonth: [],
      lastDay: null,
      loading: true,
      currentDate: moment(),
      month: {
        name: null,
        value: null,
      },
      year: null,
    };
  },
  props: {
    needUpdate: {
      type: Boolean,
      default: false,
    },
  },
  async created() {
    await this.getDate();
    await this.fetchSpecialists("?is_staff=false&is_active=true");
    await this.fetchPresence(
      `?interval_start=${`${this.year}-${
        this.month.value + 1
      }-01`}&interval_end=${`${this.year}-${this.month.value + 1}-${
        this.lastDay
      }`}`
    );
    await this.prepareData();
    this.loading = false;
  },
  methods: {
    ...mapActions({
      fetchPresence: "presence/fetchPresences",
      deletePresence: "presence/deletePresence",
      fetchSpecialists: "specialists/fetchSpecialists",
    }),
    getDate() {
      let today = this.currentDate;
      this.month.value = today.month();
      this.month.name =
        today.format("MMMM")[0].toUpperCase() + today.format("MMMM").slice(1);
      this.year = today.year();
      this.daysOfMonth = [];
      let startMonth = today.date(1);
      for (let i = 1; i <= today.daysInMonth(); i++) {
        this.daysOfMonth.push({
          num: i,
          weekend:
            startMonth.date(i).isoWeekday() === 6 ||
            startMonth.date(i).isoWeekday() === 7,
        });
      }
      this.lastDay = this.daysOfMonth[this.daysOfMonth.length - 1].num;
    },
    async changeMonth(next) {
      this.loading = true;
      if (next) {
        this.currentDate.add(1, "M");
      } else {
        this.currentDate.add(-1, "M");
      }
      await this.getDate();
      await this.fetchPresence(
        `?interval_start=${`${this.year}-${
          this.month.value + 1
        }-01`}&interval_end=${`${this.year}-${this.month.value + 1}-${
          this.lastDay
        }`}`
      );
      await this.prepareData();
      this.loading = false;
    },
    prepareData() {
      this.data = [];
      let currentDay = null;
      let value = null;
      let dateFrom = null;
      let dateTo = null;
      let displayDate = false;
      let leftBorder = false;
      let rightBorder = false;
      let dataIndex = null;
      let presenceData = null;
      for (let specialist of this.specialists) {
        this.data.push({
          key: specialist.id,
          name: `${specialist.surname} ${specialist.name[0]}.${specialist.patronymic[0]}.`,
          specialist: specialist,
        });
        dataIndex = this.data.length - 1;
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
          this.data[dataIndex][day.num] = {
            value: value,
            leftBorder: leftBorder,
            rightBorder: rightBorder,
            displayDate: displayDate,
            presence: presenceData,
          };
        }
        for (let filledDay of this.daysOfMonth) {
          if (this.data[dataIndex][filledDay.num].value !== null) {
            if (
              this.data[dataIndex][filledDay.num - 1] &&
              (this.data[dataIndex][filledDay.num - 1].value === null ||
                (this.data[dataIndex][filledDay.num - 1].value !== null &&
                  this.data[dataIndex][filledDay.num].presence.id !==
                    this.data[dataIndex][filledDay.num - 1].presence.id &&
                  this.data[dataIndex][filledDay.num].presence.id !==
                    this.data[dataIndex][filledDay.num - 1].presence
                      .main_interval_id))
            ) {
              this.data[dataIndex][filledDay.num].leftBorder = true;
              this.data[dataIndex][filledDay.num].displayDate = true;
            }
            if (
              this.data[dataIndex][filledDay.num + 1] &&
              (this.data[dataIndex][filledDay.num + 1].value === null ||
                (this.data[dataIndex][filledDay.num + 1].value !== null &&
                  this.data[dataIndex][filledDay.num].presence.id !==
                    this.data[dataIndex][filledDay.num + 1].presence.id))
            ) {
              this.data[dataIndex][filledDay.num].rightBorder = true;
              this.data[dataIndex][filledDay.num].displayDate = true;
            }
            if (
              this.data[dataIndex][filledDay.num + 1] &&
              this.data[dataIndex][filledDay.num].value === false &&
              this.data[dataIndex][filledDay.num + 1].value === true
            ) {
              this.data[dataIndex][filledDay.num].rightBorder = false;
              this.data[dataIndex][filledDay.num].displayDate = true;
              this.data[dataIndex][filledDay.num + 1].displayDate = true;
            }
          }
        }
      }
    },
    displayDeleteConfirm(item, row) {
      let that = this;
      this.$confirm({
        title: "Подтверждение удаления периода присутствия",
        content: `Специалист: ${
          row.specialist.patronymic
            ? `${row.specialist.surname} ${row.specialist.name} ${row.specialist.patronymic}`
            : `${row.specialist.surname} ${row.specialist.name}`
        }
                  Период присутсвия: ${moment(
                    item.presence.full_interval.date_from
                  ).format("DD.MM.YYYY")} - ${moment(
          item.presence.full_interval.date_to
        ).format("DD.MM.YYYY")}
                  Удалить?`,
        okType: "danger",
        onOk() {
          that.deletePresenceRecord(
            item.presence.main_interval_id === null
              ? item.presence.id
              : item.presence.main_interval_id
          );
        },
      });
    },
    async deletePresenceRecord(id) {
      try {
        let res = await this.deletePresence(id);
        if (res.status === 204) {
          this.$message.success("Период присутствия успешно удалён");
          await this.updateData();
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      }
    },
    async updateData() {
      this.loading = true;
      await this.fetchPresence(
        `?interval_start=${`${this.year}-${
          this.month.value + 1
        }-01`}&interval_end=${`${this.year}-${this.month.value + 1}-${
          this.lastDay
        }`}`
      );
      await this.prepareData();
      this.$emit("successUpdate");
      this.loading = false;
    },
  },
  computed: {
    ...mapGetters({
      presences: "presence/getPresences",
      specialists: "specialists/getSpecialists",
    }),
  },
  watch: {
    async needUpdate(value) {
      if (value === true) {
        this.updateData();
      }
    },
  },
};
</script>

<style lang="sass">
.available-table
  .ant-table-scroll
    overflow: auto
  .day
    padding: 0 !important
    .not-available, .available, .empty
      padding: 5px
      width: 100%
      height: 100%
      display: inline-block
      &:empty::before
        content: "\A0"
    .not-available
      background-color: #FFA756
      cursor: pointer
    .available
      background-color: #3DC5FF
      cursor: pointer
    .left-border
      border-top-left-radius: 4px
      border-bottom-left-radius: 4px
    .right-border
      border-top-right-radius: 4px
      border-bottom-right-radius: 4px
    .icon-button
      color: #fff
      transform: rotate(90deg)
  thead
    .day
      height: 30px
    .weekend
      background-color: #C5FF48
.title-month
  text-align: center
  margin-bottom: 10px
  .text
    padding: 0 10px
    width: 130px
    display: inline-block
    font-size: 1rem
</style>
