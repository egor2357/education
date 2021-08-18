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
    <template slot="status" slot-scope="status, item">
      <a-tag v-if="status === 0" color="cyan">Новое</a-tag>
      <template v-else-if="status === 1">
        <a-tag class="execute-block__tag" color="purple">В процессе</a-tag>
        <a
          class="execute-block__text"
          @click="setExecute(item.id)"
          v-if="
            userInfo.id === item.director.id ||
            (item.controller && userInfo.id === item.controller.id)
          "
          >Завершить</a
        >
      </template>
      <a-tag v-else-if="status === 2" color="green">Исполнено</a-tag>
    </template>
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
export default {
  name: "MissionsTable",
  mixins: [datetime, common],
  data() {
    return {
      pagination: {
        total: 0,
        page: 1,
        pageSize: 10,
        showSizeChanger: true,
        locale: { items_per_page: " на странице" },
        pageSizeOptions: ["10", "20", "30"],
      },
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
          title: "Наименование",
          dataIndex: "caption",
          key: "caption",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
          },
        },
        {
          title: "Постановщик",
          dataIndex: "director.__str__",
          key: "director_id",
          filters: [],
        },
        {
          title: "Исполнитель",
          dataIndex: "executor.__str__",
          key: "executor_id",
          filters: [],
        },
        {
          title: "Контролёр",
          dataIndex: "controller.__str__",
          key: "controller_id",
          filters: [],
        },
        {
          title: "Срок",
          dataIndex: "deadline",
          key: "deadline",
          customRender: (date) => {
            return date ? this.formatDate(date) : "";
          },
          scopedSlots: {
            filterDropdown: "filterDropdownDate",
            filterIcon: "filterIconDate",
          },
        },
        {
          title: "Статус",
          dataIndex: "status",
          key: "status",
          sorter: true,
          class: "execute-block",
          scopedSlots: { customRender: "status" },
          filters: [
            { value: 0, text: "Новое" },
            { value: 1, text: "В процессе" },
            { value: 2, text: "Исполнено" },
          ],
        },
        {
          title: "Комментарий",
          dataIndex: "comment",
          key: "comment",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
          },
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
        this.columns.splice(8);
      }
    } catch (e) {
      this.$message.error("Произошла ошибка при получении данных");
    }
  },
  methods: {
    ...mapActions({
      fetchMissions: "missions/fetchMissions",
      deleteMission: "missions/deleteMission",
      setExecuteMission: "missions/setExecuteMission",
    }),
    ...mapMutations({
      setQueryParams: "missions/setQueryParams",
    }),
    async getData() {
      this.$emit("startLoading");
      let queryString =
        `?page=${this.pagination.page}&per_page=${this.pagination.pageSize}` +
        this.filterQuery;
      this.setQueryParams(queryString);
      let res = await this.fetchMissions();
      if (res.status !== 200) {
        this.$message.error("Произошла ошибка при получении данных");
      }
      if (this.data.pagination) {
        this.pagination.total = this.data.pagination.count;
      }
      if (
        (this.filterQuery !== "" &&
          queryString !== this.$route.fullPath.replace(this.$route.path, "")) ||
        (this.filterQuery === "" &&
          this.$route.fullPath
            .replace(this.$route.path, "")
            .indexOf("ordering") !== -1)
      ) {
        this.$router.push(queryString);
      }
      this.$emit("loaded");
    },
    async tableChanged(pagination, filters, sorter) {
      this.filterQuery = "";
      this.columns.forEach((column) => {
        if (column.sortOrder && sorter.field !== column.key) {
          column.sortOrder = false;
        } else if (sorter.field === column.key && sorter.order === "descend") {
          column.sortOrder = "descend";
        } else if (sorter.field === column.key && sorter.order === "ascend") {
          column.sortOrder = "ascend";
        } else if (sorter.field === column.key && sorter.order === undefined) {
          column.sortOrder = false;
        }
      });
      if (sorter.order) {
        sorter.order === "ascend"
          ? (this.filterQuery += `&ordering=${sorter.field}`)
          : (this.filterQuery += `&ordering=-${sorter.field}`);
      }
      this.pagination.page = pagination.current;
      this.pagination.pageSize = pagination.pageSize;
      for (let key in filters) {
        if (Array.isArray(filters[key])) {
          this.filterQuery += `&${key}=${filters[key].join(",")}`;
        } else {
          this.filterQuery += `&${key}=${filters[key]}`;
        }
        this.columns.forEach((column) => {
          if (column.key === key) {
            if (filters[key] !== "") column.filteredValue = filters[key];
          }
        });
      }
      await this.getData();
    },
    displayDelete({ id, caption }) {
      let that = this;
      this.$confirm({
        title: `Поручение "${caption} будет удалено."`,
        content: `Продолжить?`,
        okType: "danger",
        onOk() {
          that.deleteRecord(id);
        },
      });
    },
    async deleteRecord(id) {
      try {
        let res = await this.deleteMission(id);
        if (res.status === 204) {
          this.$message.success("Поручение успешно удалено");
          await this.fetchMissions();
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      }
    },
    async setExecute(id) {
      try {
        let res = await this.setExecuteMission(id);
        if (res.status === 200) {
          this.$message.success("Статус поручения успешно изменён");
          await this.fetchMissions();
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      }
    },
    handleSearch(selectedKeys, confirm, dataIndex) {
      confirm();
      this.searchText = selectedKeys[0];
      this.searchedColumn = dataIndex;
    },
    handleReset(clearFilters) {
      clearFilters();
      this.searchText = "";
    },
    loadFiltersFromQuery() {
      this.filterQuery = "";
      let query = this.$route.query;
      for (let key in this.$route.query) {
        if (key === "page") {
          this.pagination.page = Number(query.page);
        } else if (key === "per_page") {
          this.pagination.pageSize = Number(query.per_page);
        } else {
          let queryValue = null;
          if (query[key].indexOf(",") !== -1) {
            queryValue = query[key].split(",");
          } else {
            queryValue = query[key];
          }
          this.columns.forEach((column) => {
            if (column.key === key) {
              if (queryValue !== "") {
                if (Array.isArray(queryValue)) {
                  column.filteredValue = queryValue.map(Number);
                } else {
                  if (this.isOnlyPositiveDigit(queryValue)) {
                    column.filteredValue = [Number(queryValue)];
                  } else {
                    column.filteredValue = [queryValue];
                  }
                }
                this.filterQuery += `&${key}=${query[key]}`;
              } else {
                column.filteredValue = [];
              }
            }
          });
        }
      }
      this.columns.forEach((column) => {
        if (
          query.ordering &&
          (query.ordering === column.key || query.ordering === `-${column.key}`)
        ) {
          if (query.ordering === column.key) {
            column.sortOrder = "ascend";
          } else if (query.ordering === `-${column.key}`) {
            column.sortOrder = "descend";
          } else if (column.sortOrder) {
            column.sortOrder = [];
          }
        }
      });
      if (query.ordering && this.filterQuery.indexOf("ordering") === -1) {
        this.filterQuery += `&ordering=${query.ordering}`;
      }
    },
  },
  computed: {
    ...mapGetters({
      data: "missions/getMissions",
      userInfo: "auth/getUserInfo",
      specialists: "specialists/getOnlySpecialists",
      admins: "specialists/getOnlyAdmins",
    }),
    specialistsForFilter() {
      return this.specialists.map((admin) => {
        return { value: admin.id, text: admin.__str__ };
      });
    },
    adminsForFilter() {
      return this.admins.map((admin) => {
        return { value: admin.id, text: admin.__str__ };
      });
    },
  },
  mounted() {
    this.$set(this.columns[2], "filters", this.adminsForFilter);
    this.$set(this.columns[3], "filters", this.specialistsForFilter);
    this.$set(this.columns[4], "filters", this.specialistsForFilter);
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
    specialistsForFilter(values) {
      this.columns[3].filters = values;
      this.columns[4].filters = values;
    },
    adminsForFilter(values) {
      this.columns[2].filters = values;
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

.missions-block
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
</style>
