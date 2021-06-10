<template>
  <a-spin :spinning="loading">
    <div class="available-table">
      <div class="top-bar">
        <a-button
          type="link"
          icon="swap"
          @click="specialist = !specialist"
          >Изменить представление</a-button
        >
        <div class="month-container">
          <a-icon class="icon-button" type="left" @click="changeMonth(false)" />
          <span class="text">{{ month.name }} {{ year }}</span>
          <a-icon class="icon-button" type="right" @click="changeMonth(true)" />
        </div>
        <a-button icon="plus" @click="$emit('onAddPeriod')">Добавить период</a-button>
      </div>
      <div class="table-presence">
        <presence-chart v-if="specialist"
          :tableData="tableData"
          :daysInMonth="daysOfMonth"
          @displayEdit="$emit('displayEdit', $event)"
          @displayDeleteConfirm="displayDeleteConfirm($event)"
        />
        <activity-presence-chart v-else
          :tableData="tableData"
          :daysInMonth="daysOfMonth"
          :activities="activities"
          @displayEdit="$emit('displayEdit', $event)"
          @displayDeleteConfirm="displayDeleteConfirm($event)"
        />
      </div>
    </div>
  </a-spin>
</template>
<script>
import moment from "moment";
import { mapGetters, mapActions } from "vuex";
import PresenceChart from "@/components/AvailableChart/PresenceChart";
import ActivityPresenceChart from "@/components/AvailableChart/ActivityPresenceChart";
import common from "@/mixins/common";
export default {
  name: "Table",
  components: { PresenceChart, ActivityPresenceChart },
  mixins: [common],
  data() {
    return {
      tableData: {specialists: []},
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
      specialist: true,
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
    await this.makeTableData();
    this.loading = false;
  },
  methods: {
    ...mapActions({
      fetchPresence: "presence/fetchPresences",
      deletePresence: "presence/deletePresence",
      fetchSpecialists: "specialists/fetchSpecialists",
      fetchActivities: "activities/fetchActivities",
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
      await this.clearSpecialistsPresent();
      await this.getDate();
      await this.fetchPresence(
        `?interval_start=${`${this.year}-${
          this.month.value + 1
        }-01`}&interval_end=${`${this.year}-${this.month.value + 1}-${
          this.lastDay
        }`}`
      );
      await this.makeTableData();
      this.loading = false;
    },
    clearSpecialistsPresent(){
      this.tableData.specialists.forEach(item => item.presence = {});
    },
    makeTableData(){
      let today = this.currentDate;
      let firstDateOfMonth = today.clone().startOf('month');
      let lastDateOfMonth = today.clone().endOf('month');
      this.tableData.specialists = this.specialists.map((spec) => {
        return {
          id: spec.id,
          fullName: spec.__str__,
          activities: spec.activities,
          hasAdditionalActivity: spec.hasAdditionalActivity,
          presence: {}
        }
      });
      for (let presence of this.presences)
      {
        let sp = this.tableData.specialists.find(item => item.id == presence.specialist_id);
        if (sp)
        {
          let firstDayOfInterval = null;
          let lastDayOfInterval = null;
          let dateFrom = moment(presence.full_interval.date_from);
          let dateTo = moment(presence.full_interval.date_to);

          let hasStart = false;
          let hasEnd = false;
          let quarantineDaysCount = 0;
          let labledDays = [];
          if (presence.main_interval_id) //это карантин
          {
            quarantineDaysCount = presence.full_interval.quarantine_days;
            if (moment(presence.date_from) < firstDateOfMonth) //и он не полностью попадает в месяц (начинается раньше)
            {
              quarantineDaysCount -= firstDateOfMonth.diff(dateFrom, 'days');
            }
            if (moment(presence.date_to) > lastDateOfMonth) //и он не полностью попадает в месяц (заканчивается позже)
            {
              quarantineDaysCount -= moment(presence.date_to).diff(lastDateOfMonth, 'days');
            }
            quarantineDaysCount = Math.max(0, quarantineDaysCount);
            if (quarantineDaysCount)
              labledDays.push(quarantineDaysCount, quarantineDaysCount + 1);
          }
          if (dateFrom < firstDateOfMonth)
          {
            firstDayOfInterval = 1;
            if (moment(presence.date_from).date() == 1)
              labledDays.push(1);
          }
          else
          {
            firstDayOfInterval = dateFrom.date();
            hasStart = true;
            labledDays.push(1);
          }
          if (dateTo > lastDateOfMonth)
          {
            lastDayOfInterval = today.daysInMonth();
          }
          else
          {
            lastDayOfInterval = dateTo.date();
            hasEnd = true;
            labledDays.push(lastDayOfInterval - firstDayOfInterval + 1);
          }
          if (presence.main_interval_id || !sp.presence[presence.id])
          {
            let intervalId = presence.main_interval_id || presence.id;
            sp.presence[intervalId] = {
              id: intervalId,
              dayFrom: firstDayOfInterval,
              daysCount: lastDayOfInterval - firstDayOfInterval + 1,
              hasStart: hasStart,
              hasEnd: hasEnd,
              quarantineDaysCount: quarantineDaysCount,
              labledDays: labledDays,
              editableData: presence
            }
          }
        }
      }
    },
    displayDeleteConfirm(data){
      let that = this
      this.$confirm({
        title: "Подтверждение удаления периода присутствия",
        content: `Специалист: ${data.specialist}
                  Период присутствия: ${moment(
                    data.presence.full_interval.date_from
                  ).format("DD.MM.YYYY")} - ${moment(
          data.presence.full_interval.date_to
        ).format("DD.MM.YYYY")}
                  Удалить?`,
        okType: "danger",
        onOk() {
          that.deletePresenceRecord(
            data.presence.main_interval_id === null
              ? data.presence.id
              : data.presence.main_interval_id
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
      await this.makeTableData();
      this.$emit("successUpdate");
      this.loading = false;
    },
  },
  computed: {
    ...mapGetters({
      presences: "presence/getPresences",
      specialists: "specialists/getSpecialists",
      activities: "activities/getActivities"
    }),
  },
  watch: {
    async needUpdate(value) {
      if (value === true) {
        await this.updateData();
      }
    },
  },
  mounted() {
    this.fetchActivities();
  },
};
</script>

<style lang="sass">
.available-table
  max-height: 100%
  display: flex
  flex-direction: column
  position: relative

  .table-presence
    flex: 1
    display: flex
    overflow: hidden

.top-bar
  margin-bottom: 10px
  display: flex
  .month-container
    flex: 1
    text-align: center
    padding-right: 70px
    font-size: 18px
    line-height: 18px
    cursor: default
  .text
    padding: 0 10px
    width: 130px
    display: inline-block
    font-size: 1rem

</style>
