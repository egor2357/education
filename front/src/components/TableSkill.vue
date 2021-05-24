<template>
  <div>
    <a-table
      :columns="columns"
      :dataSource="data"
      :bordered="true"
      :pagination="false"
      :rowKey="
        (record, index) => {
          return index;
        }
      "
      :scroll="{ y: 'calc(100vh - 310px)' }"
      :loading="tableLoading || tableLoadingActivity"
    >
      <template slot="area" slot-scope="text">
        <div class="td-label--sticky" v-if="!text.empty" :length="text.length">
          <span class="label--justify">
            {{ `${text.number}. ${text.name}` }}
          </span>
          <a-dropdown
            :trigger="['click']"
            placement="bottomLeft"
            class="dropdown--hover"
            v-if="!readOnly"
          >
            <a-icon class="icon-button" type="dash"></a-icon>
            <a-menu slot="overlay">
              <a-menu-item key="0" @click="openModalAdd(2, text)">
                Добавить направление развития
              </a-menu-item>
              <a-menu-item key="1" @click="openModalEdit(text, 1)">
                Изменить
              </a-menu-item>
              <a-menu-item key="2" @click="displayConfirmDelete(text, 1)">
                <span> Удалить </span>
              </a-menu-item>
            </a-menu>
          </a-dropdown>
        </div>
        <div class="need-delete" v-else />
      </template>
      <template slot="direction" slot-scope="text, record">
        <div class="td-label--sticky" v-if="!text.empty" :length="text.length">
          <span class="label--justify">
            {{ `${record.area.number}.${text.number}. ${text.name}` }}
          </span>
          <a-dropdown
            :trigger="['click']"
            placement="bottomLeft"
            class="dropdown--hover"
            v-if="!readOnly"
          >
            <a-icon class="icon-button" type="dash"></a-icon>
            <a-menu slot="overlay">
              <a-menu-item key="0" @click="openModalAdd(3, text)">
                Добавить навык
              </a-menu-item>
              <a-menu-item key="1" @click="openModalEdit(text, 2)">
                Изменить
              </a-menu-item>
              <a-menu-item
                key="2"
                @click="displayConfirmDelete(text, 2, record)"
              >
                <span>Удалить</span>
              </a-menu-item>
            </a-menu>
          </a-dropdown>
        </div>
        <div class="need-delete" v-else-if="record.area.empty" />
      </template>
      <template slot="skill" slot-scope="text, record">
        <div class="skill-label" v-if="!text.empty">
          <span class="label--justify">
            {{
              `${record.area.number}.${record.direction.number}.${text.number}. ${text.name}`
            }}
          </span>
          <a-dropdown
            :trigger="['click']"
            placement="bottomLeft"
            class="dropdown--hover"
            v-if="!readOnly"
          >
            <a-icon class="icon-button" type="dash"></a-icon>
            <a-menu slot="overlay">
              <a-menu-item key="1" @click="openModalEdit(text, 3)">
                Изменить
              </a-menu-item>
              <a-menu-item
                key="2"
                @click="displayConfirmDelete(text, 3, record)"
              >
                <span>Удалить</span>
              </a-menu-item>
            </a-menu>
          </a-dropdown>
        </div>
      </template>
      <template
        :slot="`activity${activity.id}`"
        slot-scope="text, record, index"
        v-for="activity in activitiesList"
      >
        <a-checkbox
          :key="activity.id"
          v-model="activityCheckboxes[activity.id][record.skill.id]"
          @change="changeLink($event, activity.id, record.skill.id)"
        />
      </template>
    </a-table>
    <a-button
      style="margin-top: 10px"
      @click="openModalAdd(1)"
      v-if="!readOnly"
    >
      Добавить образовательную область
    </a-button>
    <ModalSkills
      v-if="displayModal"
      :adding="modalAdding"
      :type="modalType"
      :editableData="modalEditableData"
      @close="displayModal = false"
      @closeSuccess="closeSuccess"
    />
  </div>
</template>

<script>
import ModalSkills from "@/components/Modals/ModalSkills";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "TableSkill",
  components: {
    ModalSkills,
  },
  props: {
    readOnly: {
      type: Boolean,
      default: false,
    },
    activities: {
      type: Boolean,
      default: false,
    },
    activitiesList: {
      type: Array,
      default: null,
    },
    tableLoadingActivity: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      columns: [
        {
          title: "Образовательная область",
          dataIndex: "area",
          width: "13%",
          scopedSlots: {
            customRender: "area",
          },
        },
        {
          title: "Направление развития",
          dataIndex: "direction",
          width: "26%",
          scopedSlots: {
            customRender: "direction",
          },
        },
        {
          title: "Навык",
          dataIndex: "skill",
          width: "61%",
          scopedSlots: {
            customRender: "skill",
          },
        },
      ],
      data: [],
      displayModal: false,
      modalAdding: true,
      modalType: 0,
      modalEditableData: {},
      tableLoading: true,
      lastNumberArea: 1,
      indexTable: 1,
      activityCheckboxes: {},
    };
  },
  async created() {
    await this.getData();
    if (this.activities) {
      this.columns[0].width = "10%";
      this.columns[1].width = "10%";
      this.columns[2].width = "30%";
      for (let activity of this.activitiesList) {
        this.columns.push({
          title: () => {
            return (
              <div title={activity.name} class="activity-title">
                <span
                  class="activity-color"
                  style={`background-color: ${activity.color}`}
                />
                <span style="flex: 0 0 calc(100% - 25px); text-align: left;">
                  {activity.name}
                </span>
              </div>
            );
          },
          dataIndex: activity,
          align: "center",
          key: `activity${activity.id}`,
          class: "vertical-header",
          scopedSlots: {
            customRender: `activity${activity.id}`,
          },
        });
      }
    }
  },
  methods: {
    ...mapActions({ fetchAreas: "skills/fetchAreas" }),
    changeDOM() {
      let elForDel = document.getElementsByClassName("need-delete");
      for (let i = elForDel.length - 1; i >= 0; i--) {
        elForDel[i].parentElement.hidden = true;
        elForDel[i].parentElement.classList.add("was-hidden");
      }
      for (let el of document.getElementsByClassName("td-label--sticky")) {
        el.parentElement.rowSpan = Number(
          !isNaN(el.attributes[0].value)
            ? el.attributes[0].value
            : el.attributes[1].value
        );
        el.parentElement.hidden = false;
        el.parentElement.classList.add("was-spanned");
      }
    },
    openModalAdd(type, item) {
      this.modalAdding = true;
      this.modalType = type;
      this.displayModal = true;
      if (type === 1) {
        this.modalEditableData.lastNumberArea = this.lastNumberArea;
      }
      if (type === 2) {
        this.modalEditableData.areaId = item.id;
        this.modalEditableData.lastNumberDirection = item.lastNumberDirection;
      }
      if (type === 3) {
        this.modalEditableData.directionId = item.id;
        this.modalEditableData.lastNumberSkill = item.lastNumberSkill;
      }
    },
    openModalEdit(item, type) {
      this.modalAdding = false;
      this.modalType = type;
      this.modalEditableData = item;
      this.displayModal = true;
    },
    async deleteRecord(item, type) {
      let dispatchName = "";
      let successMessage = "";
      this.tableLoading = true;
      if (type === 1) {
        dispatchName = "skills/deleteArea";
        successMessage = "Образовательная область успешно удалена";
      } else if (type === 2) {
        dispatchName = "skills/deleteDirection";
        successMessage = "Направление развития успешно удалено";
      } else if (type === 3) {
        dispatchName = "skills/deleteSkill";
        successMessage = "Навык успешно удален";
      } else {
        this.tableLoading = false;
        return;
      }
      try {
        let res = await this.$store.dispatch(dispatchName, item.id);
        if (res.status === 204) {
          this.$message.success(successMessage);
          await this.closeSuccess();
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      } finally {
        this.tableLoading = false;
      }
    },
    prepareData() {
      this.data = [];
      let areaObj = {};
      let directionObj = {};
      let indexStartArea = 0;
      let indexCurrentRow = 0;
      for (let area of this.areas) {
        indexStartArea = this.data.length;
        areaObj = {
          id: area.id,
          name: area.name,
          length: 1,
          number: area.number,
          empty: false,
          emptySkills: 0,
          lastNumberDirection:
            area.development_directions.length > 0
              ? area.development_directions[
                  area.development_directions.length - 1
                ].number + 1
              : 1,
        };
        this.data.push({
          area: areaObj,
          direction: { empty: true },
          skill: { empty: true },
        });
        indexCurrentRow += 1;
        let firstDirection = true;
        if (area.development_directions.length === 0) {
          this.data[indexStartArea].area.emptySkills += 1;
        }
        for (let direction of area.development_directions) {
          if (firstDirection) {
            direction.skills.length > 1
              ? (this.data[indexStartArea].area.length +=
                  direction.skills.length - 1)
              : "";
          } else {
            direction.skills.length > 1
              ? (this.data[indexStartArea].area.length +=
                  direction.skills.length)
              : (this.data[indexStartArea].area.length += 1);
          }
          directionObj = {
            id: direction.id,
            name: direction.name,
            length: direction.skills.length > 0 ? direction.skills.length : 1,
            number: direction.number,
            areaId: direction.area_id,
            lastNumberSkill:
              direction.skills.length > 0
                ? direction.skills[direction.skills.length - 1].number + 1
                : 1,
            empty: false,
          };
          if (firstDirection) {
            this.data[indexCurrentRow - 1].direction = directionObj;
            firstDirection = false;
          } else {
            this.data.push({
              area: { empty: true, number: area.number },
              direction: directionObj,
              skill: { empty: true },
            });
            indexCurrentRow += 1;
          }
          if (direction.skills.length === 0) {
            this.data[indexStartArea].area.emptySkills += 1;
          }
          let firstSkill = true;
          for (let skill of direction.skills) {
            if (firstSkill) {
              this.data[indexCurrentRow - 1].skill = {
                id: skill.id,
                name: skill.name,
                number: skill.number,
                directionId: skill.direction_id,
                empty: false,
              };
              firstSkill = false;
            } else {
              this.data.push({
                area: { empty: true, number: area.number },
                direction: { empty: true, number: direction.number },
                skill: {
                  id: skill.id,
                  name: skill.name,
                  number: skill.number,
                  directionId: skill.direction_id,
                  empty: false
                },
              });
              indexCurrentRow += 1;
            }
          }
        }
      }
      if (this.areas.length > 0) {
        this.lastNumberArea = this.areas[this.areas.length - 1].number + 1;
      }
    },
    async getData() {
      this.tableLoading = true;
      await this.fetchAreas();
      await this.prepareData();
      if (this.activities) await this.prepareDataForActivities();
      if (this.activities) await this.prepareActivityCheckboxes();
      await this.changeDOM();
      this.tableLoading = false;
    },
    displayConfirmDelete(text, type, record) {
      let title = "";
      let content = "";
      if (type === 1) {
        title = `Вы действительно хотите удалить образовательную область "${text.number}.${text.name}"?`;
        content = "Будут удалены все связанные направления развития и навыки.";
      } else if (type === 2) {
        title = `Вы действительно хотите удалить направление развития "${record.area.number}.${text.number}.${text.name}"?`;
        content = "Будут удалены все связанные навыки.";
      } else if (type === 3) {
        title = `Вы действительно хотите удалить навык "${record.area.number}.${record.direction.number}.${text.number}.${text.name}?"`;
        content = "";
      }
      let that = this;
      this.$confirm({
        title: title,
        content: content,
        okType: "danger",
        onOk() {
          that.deleteRecord(text, type);
        },
      });
    },
    closeSuccess() {
      this.displayModal = false;
      let elWasHidden = document.getElementsByClassName("was-hidden");
      for (let i = elWasHidden.length - 1; i >= 0; i--) {
        elWasHidden[i].hidden = false;
        elWasHidden[i].classList.remove("was-hidden");
      }
      let elWasSpanned = document.getElementsByClassName("was-spanned");
      for (let i = elWasSpanned.length - 1; i >= 0; i--) {
        elWasSpanned[i].rowSpan = 1;
        elWasSpanned[i].classList.remove("was-spanned");
      }
      this.getData();
    },
    prepareDataForActivities() {
      let index = 0;
      let deleted = false;
      let len = this.data.length;
      let element = {};
      let savedArea = {};
      for (index; index < len; ) {
        deleted = false;
        if (this.data[index]) {
          element = this.data[index];
          element.area.empty === false
            ? (element.area.length -= element.area.emptySkills)
            : "";
        } else {
          break;
        }
        if (
          (element.skill.empty === true && element.area.empty === true) ||
          (element.skill.empty === true && element.direction.empty === true) ||
          (element.skill.empty === true &&
            element.direction.empty !== true &&
            element.direction.area !== true)
        ) {
          if (element.skill.empty === true && element.area.empty === false) {
            savedArea = element.area;
          }
          this.data.splice(index, 1);
          deleted = true;
        } else if(element.skill.empty === false && element.area.empty === true && element.direction.empty === false) {
          if (this.data[index - 1] && element.direction.areaId === savedArea.id && this.data[index - 1].direction.areaId !== savedArea.id) {
            element.area = savedArea
          }
        }
        deleted === false ? (index += 1) : "";
      }
    },
    prepareActivityCheckboxes() {
      if (Object.keys(this.activitiesCheckboxes).length === 0) {
        for (let activity of this.activitiesList) {
          this.$set(this.activityCheckboxes, activity.id, {});
          for (let element of this.data) {
            this.$set(
              this.activityCheckboxes[activity.id],
              element.skill.id,
              activity.skills.indexOf(element.skill.id) !== -1
            );
          }
        }
        this.$store.commit(
          "activities/setActivitiesCheckboxes",
          this.activityCheckboxes
        );
      } else {
        this.activityCheckboxes = this.activitiesCheckboxes;
      }
    },
    changeLink(event, activityId, skillId) {
      this.$emit("changeLink", {
        activityId: activityId,
        skillId: skillId,
        value: event.target.checked,
      });
    },
  },
  computed: {
    ...mapGetters({
      areas: "skills/getAreas",
      activitiesCheckboxes: "activities/getActivitiesCheckboxes",
    }),
  },
};
</script>

<style lang="sass">
.td-label--sticky, .skill-label
  position: -webkit-sticky
  position: sticky
  top: 0
  display: flex
  .label--justify
    flex: 0 0 98%
.ant-table-tbody > tr:hover:not(.ant-table-expanded-row):not(.ant-table-row-selected) > td
  background-color: unset
.ant-table-row
  td
    vertical-align: baseline
    &:hover
      background-color: #e6f7ff !important

.ant-table-row
  td
    .dropdown--hover
      display: none
      flex: 0 0 2%
      height: 20px
      svg
        transform: rotate(90deg)
        margin-top: 3px
    &:hover
      .dropdown--hover
        display: unset

/*.ant-table-body*/
  /*overflow-y: auto !important*/
/*.ant-table-header*/
  /*overflow: auto !important*/
  /*margin-bottom: 0 !important*/
  /*padding-right: 16px*/

.vertical-header
  padding: 5px !important
  vertical-align: middle !important
  .ant-table-header-column
    writing-mode: vertical-rl
    transform: rotate(180deg)
    max-height: 180px
    height: 100%
    .activity-title
      display: flex
      overflow: hidden
      text-overflow: ellipsis
      max-width: 40px
      .activity-color
        width: 20px
        height: 20px
        border-radius: 20px
        flex: 0 0 20px
        align-self: center
        margin-bottom: 5px
</style>
