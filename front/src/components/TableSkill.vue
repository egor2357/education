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
      :scroll="{y: 'calc(100vh - 260px)'}"
    >
      <template slot="area" slot-scope="text">
        <div class="td-label--sticky" v-if="!text.empty" :length="text.length">
          {{ `${text.index}. ${text.name}` }}
        </div>
        <div class="need-delete" v-else />
      </template>
      <template slot="direction" slot-scope="text, record">
        <div class="td-label--sticky" v-if="!text.empty" :length="text.length">
          {{ `${record.area.index}.${text.index}. ${text.name}` }}
        </div>
        <div class="need-delete" v-else />
      </template>
    </a-table>
  </div>
</template>

<script>
export default {
  name: "TableSkill",
  data() {
    return {
      columns: [
        {
          title: "Образовательная область",
          dataIndex: "area",
          width: "13%",
          // customRender: (text) => {
          //   let obj = {
          //     children:`${text.index}. ${text.name}`,
          //     attrs: {}
          //   };
          //   if (!text.empty) {
          //     obj.attrs.rowSpan = text.length;
          //   } else {
          //     obj.attrs.rowSpan = 0;
          //   }
          //   return obj
          // },
          scopedSlots: {
            customRender: "area",
          },
        },
        {
          title: "Направление развития",
          dataIndex: "direction",
          width: "26%",
          // customRender: (text, record) => {
          //   let obj = {
          //     children: `${record.area.index}.${text.index}. ${text.name}`,
          //     attrs: {},
          //   };
          //   if (!text.empty) {
          //     obj.attrs.rowSpan = text.length;
          //   } else {
          //     obj.attrs.rowSpan = 0;
          //   }
          //   return obj;
          // },
          scopedSlots: {
            customRender: "direction",
          },
        },
        {
          title: "Навык",
          dataIndex: "skill",
          width: "61%",
          customRender: (text, record) => {
            return `${record.area.index}.${record.direction.index}.${text.index}. ${text.name}`;
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
    };
  },
  created() {
    for (let i = 0; i < 5; i++) {
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

</style>
