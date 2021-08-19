<template>
  <a-table
    :columns="columns"
    :dataSource="data.results"
    bordered
    :rowKey="'id'"
    :pagination="pagination"
    @change="tableChanged"
    :locale="{
      filterReset: 'Отменить',
      filterConfirm: 'Поиск',
    }"
  >
    <span slot="actions" slot-scope="text, item">
      <div class="flex-column">
        <a @click="$emit('displayEdit', item)" v-if="item.status !== 2">
          Изменить
        </a>
        <a @click="displayDelete(item)">Удалить</a>
      </div>
    </span>
    <div
      slot="filterDropdown"
      slot-scope="{
        setSelectedKeys,
        selectedKeys,
        confirm,
        clearFilters,
        column,
      }"
      class="filter-dropdown"
    >
      <a-input
        v-ant-ref="(c) => (searchInput = c)"
        :placeholder="`Поиск ${column.title}`"
        :value="selectedKeys[0]"
        class="text-input"
        @change="(e) => setSelectedKeys(e.target.value ? [e.target.value] : [])"
        @pressEnter="
          () => handleSearch(selectedKeys, confirm, column.dataIndex)
        "
      />
      <a-button
        type="primary"
        icon="search"
        size="small"
        class="search-button"
        @click="() => handleSearch(selectedKeys, confirm, column.dataIndex)"
      >
        Поиск
      </a-button>
      <a-button
        size="small"
        class="cancel-button"
        @click="() => handleReset(clearFilters)"
      >
        Отменить
      </a-button>
    </div>
    <a-icon
      slot="filterIcon"
      slot-scope="filtered"
      type="search"
      :style="{ color: filtered ? '#108ee9' : undefined }"
    />
    <div
      slot="filterDropdownDate"
      slot-scope="{
        setSelectedKeys,
        selectedKeys,
        confirm,
        clearFilters,
        column,
      }"
      class="filter-dropdown"
    >
      <a-date-picker
        v-ant-ref="(c) => (searchInput = c)"
        :placeholder="`Поиск ${column.title}`"
        :value="selectedKeys[0]"
        format="DD.MM.YYYY"
        class="date-input"
        @change="
          (e) =>
            setSelectedKeys(
              e !== null
                ? [
                    `${e._d.getFullYear()}-${
                      e._d.getMonth() + 1
                    }-${e._d.getDate()}`,
                  ]
                : []
            )
        "
        @pressEnter="
          () => handleSearch(selectedKeys, confirm, column.dataIndex)
        "
      ></a-date-picker>
      <a-button
        type="primary"
        icon="search"
        size="small"
        class="search-button"
        @click="() => handleSearch(selectedKeys, confirm, column.dataIndex)"
      >
        Поиск
      </a-button>
      <a-button
        size="small"
        class="cancel-button"
        @click="() => handleReset(clearFilters)"
      >
        Отменить
      </a-button>
    </div>
    <a-icon
      slot="filterIconDate"
      slot-scope="filtered"
      type="calendar"
      :style="{ color: filtered ? '#108ee9' : undefined }"
    />
  </a-table>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from "vuex";
import datetime from "@/mixins/datetime";
import common from "@/mixins/common";
import tableFilterSort from "@/mixins/tableFilterSort";
export default {
  name: "TaskGroupsTable",
  mixins: [datetime, common, tableFilterSort],
  props: {
    questionsSelected: Boolean,
  },
  data() {
    return {
      columns: [
        {
          title: "Дата",
          dataIndex: "creation_date",
          key: "creation_date",
          sorter: true,
          customRender: (date) => {
            return date ? this.formatDate(date) : "";
          },
          scopedSlots: {
            filterDropdown: "filterDropdownDate",
            filterIcon: "filterIconDate",
          },
        },
        {
          title: "Содержание",
          dataIndex: "text",
          key: "text",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
          },
          class: "pre-wrap",
        },
        {
          title: "Автор",
          dataIndex: "author.__str__",
          key: "author_id",
          filters: [],
        },
        {
          title: "Ответственный",
          dataIndex: "responsible.__str__",
          key: "responsible_id",
          filters: [],
        },
        {
          title: "Срок",
          dataIndex: "deadline",
          key: "deadline",
          sorter: true,
          customRender: (date) => {
            return date ? this.formatDate(date) : "";
          },
          scopedSlots: {
            filterDropdown: "filterDropdownDate",
            filterIcon: "filterIconDate",
          },
        },
        {
          title: "Решение",
          dataIndex: "solution",
          key: "solution",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
          },
          class: "pre-wrap",
        },
        {
          title: "Действия",
          dataIndex: "actions",
          key: "actions",
          scopedSlots: { customRender: "actions" },
        },
      ],
      filterQuery: "",
    };
  },
  async created() {
    try {
      this.loadFiltersFromQuery();
      await this.getData();
      if (!this.userInfo.staff) {
        this.columns.splice(6);
      }
    } catch (e) {
      this.$message.error("Произошла ошибка при получении данных");
    }
  },
  methods: {
    ...mapActions({
      fetchTaskGroups: "taskGroups/fetchTaskGroups",
      deleteTaskGroup: "taskGroups/deleteTaskGroup",
    }),
    ...mapMutations({
      setQueryParams: "taskGroups/setQueryParams",
    }),
    async getData(questionsSelected = this.questionsSelected) {
      this.$emit("startLoading");
      let queryString =
        `?page=${this.pagination.page}&per_page=${
          this.pagination.pageSize
        }&is_question=${questionsSelected === true}` + this.filterQuery;
      this.setQueryParams(queryString);
      let res = await this.fetchTaskGroups();
      if (res.status !== 200) {
        this.$message.error("Произошла ошибка при получении данных");
      }
      this.updatePaginationTotal();
      this.routerCheckAndPush(queryString);
      this.$emit("loaded");
    },
    displayDelete({ id, text }) {
      let that = this;
      this.$confirm({
        title: `Интервенционная группа "${text} будет удалена."`,
        content: `Продолжить?`,
        okType: "danger",
        onOk() {
          that.deleteRecord(id);
        },
      });
    },
    async deleteRecord(id) {
      try {
        let res = await this.deleteTaskGroup(id);
        if (res.status === 204) {
          this.$message.success("Интервенционная группа успешно удалена");
          await this.fetchTaskGroups();
          this.updatePaginationTotal();
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      }
    },
  },
  computed: {
    ...mapGetters({
      data: "taskGroups/getTaskGroups",
      userInfo: "auth/getUserInfo",
      onlySpecialists: "specialists/getOnlySpecialists",
      allSpecialists: "specialists/getSpecialists",
    }),
    onlySpecialistsForFilter() {
      return this.onlySpecialists.map((admin) => {
        return { value: admin.id, text: admin.__str__ };
      });
    },
    allSpecialistsForFilter() {
      return this.allSpecialists.map((admin) => {
        return { value: admin.id, text: admin.__str__ };
      });
    },
  },
  mounted() {
    if (this.userInfo.staff) {
      this.$set(this.columns[2], "filters", this.allSpecialistsForFilter);
      this.$set(this.columns[3], "filters", this.onlySpecialistsForFilter);
    }
    window.onpopstate = function () {
      this.columns.forEach((column) => {
        column.filteredValue = [];
        column.sortOrder = false;
      });
      this.loadFiltersFromQuery();
      this.getData();
    }.bind(this);
  },
  watch: {
    allSpecialistsForFilter(values) {
      if (this.userInfo.staff) {
        this.columns[2].filters = values;
      }
    },
    onlySpecialistsForFilter(values) {
      if (this.userInfo.staff) {
        this.columns[3].filters = values;
      }
    },
  },
};
</script>

<style lang="sass">
.ant-table-filter-dropdown
  min-width: 150px

  .ant-dropdown-menu
    max-height: 300px

.filter-dropdown
  padding: 8px

  .text-input
    width: 188px
    margin-bottom: 8px
    display: block
  .search-button
    width: 90px
    margin-right: 8px
  .cancel-button
    width: 90px

  .date-input
    width: 200px
    margin-bottom: 8px
    display: block

.task-groups-block
  .ant-table-thead
    .ant-table-header-column
      .ant-table-column-sorters
        display: flex
      .ant-table-column-title
        order: 2
      .ant-table-column-sorter
        align-self: center
        .ant-table-column-sorter-inner
          margin-right: 0.57142857em
          margin-left: 0

  .ant-table-tbody
    .execute-block
      text-align: center
      max-width: 120px
      .execute-block__tag
        margin-bottom: 5px
        margin-right: 0
      .execute-block__text
        font-size: 0.8rem
    .pre-wrap
      white-space: pre-wrap
</style>
