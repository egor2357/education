<template>
  <div
    class="specialist-presence"
    :class="{ 'specialist-presence--one': specReadOnly }"
  >
    <a-spin :spinning="loading">
      <div class="presence-container">
        <div class="top-bar" v-if="!specReadOnly">
          <div class="top-bar__side-block left">
            <a-button
              type="link"
              icon="swap"
              @click="specialistMode = !specialistMode"
              >Изменить представление</a-button
            >
          </div>
          <div class="title">График присутствия специалистов</div>
          <div class="top-bar__side-block right">
            <a-button v-if="isStaff" icon="plus" @click="onAddPeriod"
              >Добавить период</a-button
            >
          </div>
        </div>
        <div class="month-container">
          <a-icon class="icon-button" type="left" @click="changeMonth(false)" />
          <span class="text">{{ monthLabel }}</span>
          <a-icon class="icon-button" type="right" @click="changeMonth(true)" />
        </div>

        <div class="table-presence">
          <presence-chart
            v-if="specialistMode"
            :tableData="tableData"
            :specReadOnly="specReadOnly"
            :is-staff="isStaff"
            @displayEdit="displayEdit"
            @displayEditSummary="displayEditSummary"
            @displayDeleteConfirm="displayDeleteConfirm($event)"
          />

          <activity-presence-chart
            v-else
            :tableData="tableData"
            :activities="activities"
            :is-staff="isStaff"
            @displayEdit="displayEdit"
            @displayEditSummary="displayEditSummary"
            @displayDeleteConfirm="displayDeleteConfirm($event)"
          />
        </div>
        <ModalPeriod
          v-if="displayModal"
          :editableData="modalEditableData"
          :adding="modalAdding"
          @close="displayModal = false"
          @closeSuccess="
            displayModal = false;
            updateData();
          "
        />
        <ModalSummary
          v-if="showEditSummary"
          :editableData="modalEditableData"
          :editableSpecialist="editableSpecialist"
          :is-staff="isStaff || (modalEditableData.presence.specialist_id == specialistId)"
          @close="closeSummaryModal($event)"
        />
      </div>
    </a-spin>
  </div>
</template>

<script>
import moment from "moment";
import ModalPeriod from "@/components/AvailableChart/ModalPeriod";
import ModalSummary from "@/components/AvailableChart/ModalSummary";
import PresenceChart from "@/components/AvailableChart/PresenceChart";
import ActivityPresenceChart from "@/components/AvailableChart/ActivityPresenceChart";
import { mapGetters, mapActions } from "vuex";
export default {
  name: "AvailableChart",
  components: {
    ModalPeriod,
    ModalSummary,
    PresenceChart,
    ActivityPresenceChart,
  },
  props: {
    specReadOnly: {
      type: Boolean,
      default: false,
    },
    userId: {
      type: [Number, String],
      default: null,
    },
  },
  data() {
    return {
      displayModal: false,
      showEditSummary: false,
      modalEditableData: {},
      editableSpecialist: '',
      modalAdding: true,
      specialistMode: true,
      loading: true,
      currentDate: moment(),
      monthLabel:
        moment().format("MMMM")[0].toUpperCase() +
        moment().format("MMMM").slice(1) +
        "  " +
        moment().year(),
      tableData: { daysInMonth: [], specialists: [] },
    };
  },
  computed: {
    ...mapGetters({
      presences: "presence/getPresences",
      specialists: "specialists/getSpecialists",
      activities: "activities/getActivities",
      activitiesFetched: "activities/getFetched",
    }),
    isStaff() {
      return this.$store.getters["auth/getUserInfo"].staff;
    },
    specialistId(){
      return this.$store.getters["auth/getUserInfo"].specialistId;
    }
  },
  async created() {
    await this.fetchSpecialists("?is_staff=false&is_active=true");

    await this.fetchPresence(
      `?interval_start=${`${this.currentDate.year()}-${
        this.currentDate.month() + 1
      }-01`}&interval_end=${`${this.currentDate.year()}-${
        this.currentDate.month() + 1
      }-${this.currentDate.daysInMonth()}`}`
    );

    if (!this.activitiesFetched) await this.fetchActivities();
    this.makeTableData();
    this.loading = false;
    if (!this.specReadOnly) {
      document.addEventListener("keydown", this.keydown);
    }
  },
  methods: {
    ...mapActions({
      fetchPresence: "presence/fetchPresences",
      deletePresence: "presence/deletePresence",
      fetchSpecialists: "specialists/fetchSpecialists",
      fetchActivities: "activities/fetchActivities",
    }),
    async changeMonth(next) {
      this.loading = true;
      if (next) {
        this.currentDate.add(1, "M");
      } else {
        this.currentDate.add(-1, "M");
      }
      await this.fetchPresence(
        `?interval_start=${`${this.currentDate.year()}-${
          this.currentDate.month() + 1
        }-01`}&interval_end=${`${this.currentDate.year()}-${
          this.currentDate.month() + 1
        }-${this.currentDate.daysInMonth()}`}`
      );
      await this.makeTableData();
      this.loading = false;
    },
    makeTableData() {
      this.monthLabel =
        this.currentDate.format("MMMM")[0].toUpperCase() +
        this.currentDate.format("MMMM").slice(1) +
        "  " +
        this.currentDate.year();
      let today = this.currentDate.clone();
      this.tableData.daysInMonth = [];
      let startMonth = today.date(1);
      for (let i = 1; i <= today.daysInMonth(); i++) {
        this.tableData.daysInMonth.push({
          num: i,
          weekend:
            startMonth.date(i).isoWeekday() === 6 ||
            startMonth.date(i).isoWeekday() === 7,
        });
      }
      let firstDateOfMonth = today.clone().startOf("month");
      let lastDateOfMonth = today.clone().endOf("month");

      if (this.specReadOnly) {
        let findRes = this.specialists.find(
          (spec) => spec.user.id == this.userId
        );
        findRes
          ? (this.tableData.specialists = [findRes].map((spec) => {
              return {
                id: spec.id,
                fullName: spec.__str__,
                activities: spec.activities,
                hasAdditionalActivity: spec.hasAdditionalActivity,
                presence: {},
              };
            }))
          : (this.tableData.specialists = []);
      } else {
        this.tableData.specialists = this.specialists.map((spec) => {
          return {
            id: spec.id,
            fullName: spec.__str__,
            activities: spec.activities,
            hasAdditionalActivity: spec.hasAdditionalActivity,
            presence: {},
          };
        });
      }
      for (let presence of this.presences) {
        let sp = this.tableData.specialists.find(
          (item) => item.id == presence.specialist_id
        );
        if (sp) {
          let firstDayOfInterval = null;
          let lastDayOfInterval = null;
          let dateFrom = moment(presence.full_interval.date_from);
          let dateTo = moment(presence.full_interval.date_to);

          let hasStart = false;
          let hasEnd = false;
          let quarantineDaysCount = 0;
          let labledDays = [];
          if (presence.main_interval_id) {
            //это карантин
            quarantineDaysCount = presence.full_interval.quarantine_days;
            if (moment(presence.date_from) < firstDateOfMonth) {
              //и он не полностью попадает в месяц (начинается раньше)
              quarantineDaysCount -= firstDateOfMonth.diff(dateFrom, "days");
            }
            if (moment(presence.date_to) > lastDateOfMonth) {
              //и он не полностью попадает в месяц (заканчивается позже)
              quarantineDaysCount -= moment(presence.date_to).diff(
                lastDateOfMonth,
                "days"
              );
            }
            quarantineDaysCount = Math.max(0, quarantineDaysCount);
            if (quarantineDaysCount)
              labledDays.push(quarantineDaysCount, quarantineDaysCount + 1);
          }
          if (dateFrom < firstDateOfMonth) {
            firstDayOfInterval = 1;
            if (
              moment(presence.date_from).date() == 1 &&
              firstDateOfMonth.month() == moment(presence.date_from).month()
            ) {
              //проверка на старт присутствия в первый день месяца после карантина
              labledDays.push(1);
            }
          } else {
            firstDayOfInterval = dateFrom.date();
            hasStart = true;
            labledDays.push(1);
          }
          if (dateTo > lastDateOfMonth) {
            lastDayOfInterval = today.daysInMonth();
          } else {
            lastDayOfInterval = dateTo.date();
            hasEnd = true;
            labledDays.push(lastDayOfInterval - firstDayOfInterval + 1);
          }
          if (presence.main_interval_id || !sp.presence[presence.id]) {
            let intervalId = presence.main_interval_id || presence.id;
            sp.presence[intervalId] = {
              id: intervalId,
              dayFrom: firstDayOfInterval,
              daysCount: lastDayOfInterval - firstDayOfInterval + 1,
              hasStart: hasStart,
              hasEnd: hasEnd,
              quarantineDaysCount: quarantineDaysCount,
              labledDays: labledDays,
              editableData: presence,
            };
          }
        }
      }
    },
    displayEdit(item) {
      this.modalEditableData = item;
      this.modalAdding = false;
      this.displayModal = true;
    },
    displayEditSummary(item) {
      this.modalEditableData = item;
      let specialist = this.specialists.find(spec => spec.id == item.presence.specialist_id);
      if (specialist)
        this.editableSpecialist = specialist.__str__;
      else
        this.editableSpecialist = '';
      this.showEditSummary = true;
    },
    onAddPeriod() {
      this.modalAdding = true;
      this.modalEditableData = {};
      this.displayModal = true;
    },
    displayDeleteConfirm(data) {
      let that = this;
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
        `?interval_start=${`${this.currentDate.year()}-${
          this.currentDate.month() + 1
        }-01`}&interval_end=${`${this.currentDate.year()}-${
          this.currentDate.month() + 1
        }-${this.currentDate.daysInMonth()}`}`
      );
      await this.makeTableData();
      this.loading = false;
    },
    closeSummaryModal(isSuccess = false) {
      this.showEditSummary = false;
      if (isSuccess) {
        this.updateData();
      }
    },
    keydown(event) {
      if (event.type === "keydown" && event.keyCode === 39) {
        this.changeMonth(true);
      } else if (event.type === "keydown" && event.keyCode === 37) {
        this.changeMonth(false);
      }
    },
  },
  beforeDestroy() {
    document.removeEventListener("keydown", this.keydown);
  },
};
</script>

<style lang="sass">
.presence-container
  display: flex
  flex-direction: column
  height: 100%
.specialist-presence
  display: flex
  flex-direction: column
  height: 100%
  overflow: hidden
  &--one
    height: auto
    min-height: 140px

    .presence-chart__table-body-chart-holder
      margin: 5px 10px

    .presence-chart__table-body-row:hover
      background: transparent

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

  .month-container
    text-align: center
    font-size: 18px
    line-height: 18px
    cursor: default
    line-height: 32px
    margin-bottom: 10px

    .text
      padding: 0 10px
      width: 140px
      display: inline-block
      font-size: 1rem

  .table-presence
    flex: 1
    display: flex
    overflow: hidden
</style>
