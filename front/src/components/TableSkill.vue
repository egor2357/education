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
      :scroll="{ y: 'calc(100vh - 260px)' }"
    >
      <template slot="area" slot-scope="text">
        <div class="td-label--sticky" v-if="!text.empty" :length="text.length">
          <span>
            {{ `${text.index}. ${text.name}` }}
          </span>
          <a-dropdown
            :trigger="['click']"
            placement="bottomLeft"
            class="dropdown--hover"
          >
            <a-icon class="icon-button" type="dash"></a-icon>
            <a-menu slot="overlay">
              <a-menu-item key="1" @click="openModalEdit(text, 1)">
                Изменить
              </a-menu-item>
              <a-menu-item key="2">
                <a-popconfirm
                  title="Вы действительно хотите удалить данную область?"
                  ok-text="Да"
                  cancel-text="Нет"
                  @confirm="deleteRecord(text, 1)"
                >
                  <span>Удалить</span>
                </a-popconfirm>
              </a-menu-item>
            </a-menu>
          </a-dropdown>
        </div>
        <div class="need-delete" v-else />
      </template>
      <template slot="direction" slot-scope="text, record">
        <div class="td-label--sticky" v-if="!text.empty" :length="text.length">
          <span>
            {{ `${record.area.index}.${text.index}. ${text.name}` }}
          </span>
          <a-dropdown
            :trigger="['click']"
            placement="bottomLeft"
            class="dropdown--hover"
          >
            <a-icon class="icon-button" type="dash"></a-icon>
            <a-menu slot="overlay">
              <a-menu-item key="1" @click="openModalEdit(text, 2)">
                Изменить
              </a-menu-item>
              <a-menu-item key="2">
                <a-popconfirm
                  title="Вы действительно хотите удалить данное направление?"
                  ok-text="Да"
                  cancel-text="Нет"
                  @confirm="deleteRecord(text, 2)"
                >
                  <span>Удалить</span>
                </a-popconfirm>
              </a-menu-item>
            </a-menu>
          </a-dropdown>
        </div>
        <div class="need-delete" v-else />
      </template>
      <template slot="skill" slot-scope="text, record">
        <div>
          <span>
            {{
              `${record.area.index}.${record.direction.index}.${text.index}. ${text.name}`
            }}
          </span>
          <a-dropdown
            :trigger="['click']"
            placement="bottomLeft"
            class="dropdown--hover"
          >
            <a-icon class="icon-button" type="dash"></a-icon>
            <a-menu slot="overlay">
              <a-menu-item key="1" @click="openModalEdit(text, 3)">
                Изменить
              </a-menu-item>
              <a-menu-item key="2">
                <a-popconfirm
                  title="Вы действительно хотите удалить данный навык?"
                  ok-text="Да"
                  cancel-text="Нет"
                  @confirm="deleteRecord(text, 3)"
                >
                  <span>Удалить</span>
                </a-popconfirm>
              </a-menu-item>
            </a-menu>
          </a-dropdown>
        </div>
      </template>
    </a-table>
    <ModalSkills
      v-if="displayModal"
      :adding="modalAdding"
      :type="modalType"
      :editableData="modalEditableData"
      @close="displayModal = false"
    />
  </div>
</template>

<script>
import ModalSkills from "@/components/Modals/ModalSkills";
export default {
  name: "TableSkill",
  components: {
    ModalSkills,
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
      data: [
        {
          area: { name: "Область 1", index: 1, length: 10, empty: false },
          direction: {
            name: "Направление 1",
            index: 1,
            length: 7,
            empty: false,
          },
          skill: { name: "Навык 1. ", index: 1 },
        },
        {
          area: { empty: true, index: 1 },
          direction: { empty: true, index: 1 },
          skill: { name: "Навык 2", index: 2 },
        },
        {
          area: { empty: true, index: 1 },
          direction: { empty: true, index: 1 },
          skill: { name: "Навык 3", index: 3 },
        },
        {
          area: { empty: true, index: 1 },
          direction: { empty: true, index: 1 },
          skill: { name: "Навык 4", index: 4 },
        },
        {
          area: { empty: true, index: 1 },
          direction: { empty: true, index: 1 },
          skill: { name: "Навык 5", index: 5 },
        },
        {
          area: { empty: true, index: 1 },
          direction: { empty: true, index: 1 },
          skill: { name: "Навык 6", index: 6 },
        },
        {
          area: { empty: true, index: 1 },
          direction: { empty: true, index: 1 },
          skill: { name: "Навык 7", index: 7 },
        },
        {
          area: { empty: true, index: 1 },
          direction: {
            name: "Направление 2",
            index: 2,
            length: 3,
            empty: false,
          },
          skill: { name: "Навык 8", index: 1 },
        },
        {
          area: { empty: true, index: 1 },
          direction: { empty: true, index: 2 },
          skill: { name: "Навык 9", index: 2 },
        },
        {
          area: { empty: true, index: 1 },
          direction: { empty: true, index: 2 },
          skill: { name: "Навык 10", index: 3 },
        },
      ],
      displayModal: false,
      modalAdding: true,
      modalType: 0,
      modalEditableData: {},
    };
  },
  created() {
    for (let i = 0; i < 2; i++) {
      this.data = this.data.concat(this.data);
    }
  },
  mounted() {
    this.testMethod();
  },
  methods: {
    testMethod() {
      for (let el of document.getElementsByClassName("td-label--sticky")) {
        el.parentElement.rowSpan = Number(el.attributes[0].value);
      }
      let elForDel = document.getElementsByClassName("need-delete");
      let lengthForDel = elForDel.length;
      for (let i = lengthForDel - 1; i >= 0; i--) {
        elForDel[i].parentNode.remove();
      }
    },
    openModalEdit(item, type) {
      this.modalAdding = false;
      this.modalType = type;
      this.modalEditableData = item;
      this.displayModal = true;
    },
    deleteRecord(item, type) {
      console.log(type);
      console.log(item);
    },
  },
};
</script>

<style lang="sass">
.td-label--sticky
  position: -webkit-sticky
  position: sticky
  top: 0
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
    &:hover
      .dropdown--hover
        display: unset
</style>
