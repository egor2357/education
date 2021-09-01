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
    <template slot="theme" slot-scope="theme, item">
      <a @click.prevent="goToDetail(item)">{{ theme }}</a>
      <div class="message-count" v-if="item.count_unreaded">
        Непрочитанных сообщений: {{ item.count_unreaded }}
      </div>
    </template>
    <template slot="status" slot-scope="closed">
      <a-tag class="status-block__tag" color="blue" v-if="!closed"
        >Открыто</a-tag
      >
      <a-tag class="status-block__tag" color="green" v-else>Закрыто</a-tag>
    </template>
    <span slot="actions" slot-scope="text, item">
      <div class="flex-column">
        <a @click="displayDelete(item)">Удалить</a>
      </div>
    </span>
  </a-table>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from "vuex";
import datetime from "@/mixins/datetime";
import common from "@/mixins/common";
import tableFilterSort from "@/mixins/tableFilterSort";
export default {
  name: "AppealsTable",
  mixins: [datetime, common, tableFilterSort],
  data() {
    return {
      columns: [
        {
          title: "Дата",
          dataIndex: "creation_date",
          key: "creation_date",
          sorter: true,
          width: "140px",
          customRender: (date) => {
            return date ? this.formatDate(date) : "";
          },
          scopedSlots: {
            filterDropdown: "filterDropdownDate",
            filterIcon: "filterIconDate",
          },
        },
        {
          title: "Тема",
          dataIndex: "theme",
          key: "theme",
          filters: [],
          class: "pre-wrap theme-block",
          scopedSlots: {
            customRender: "theme",
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
          },
        },
        {
          title: "Статус",
          dataIndex: "closed",
          key: "closed",
          filters: [
            { value: 0, text: "Открыто" },
            { value: 1, text: "Закрыто" },
          ],
          class: "status-block",
          width: "120px",
          scopedSlots: {
            customRender: "status",
          },
        },
        {
          title: "Специалист",
          dataIndex: "creator.__str__",
          key: "creator_id",
          filters: [],
          sorter: true,
          width: "250px",
        },
        {
          title: "Действия",
          dataIndex: "actions",
          key: "actions",
          width: "120px",
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
      await this.fetchNotifications();
      if (!this.userInfo.staff) {
        this.columns.splice(3);
        this.columns.splice(4);
      }
    } catch (e) {
      this.$message.error("Произошла ошибка при получении данных");
    }
  },
  methods: {
    ...mapActions({
      fetchAppeals: "appeals/fetchAppeals",
      deleteAppeal: "appeals/deleteAppeal",
      fetchNotifications: "notifications/fetchNotifications",
    }),
    ...mapMutations({
      setQueryParams: "appeals/setQueryParams",
    }),
    async getData() {
      this.$emit("startLoading");
      let queryString =
        `?page=${this.pagination.page}&per_page=${this.pagination.pageSize}` +
        this.filterQuery;
      this.setQueryParams(queryString);
      let res = await this.fetchAppeals();
      if (res.status !== 200) {
        this.$message.error("Произошла ошибка при получении данных");
      }
      this.updatePaginationTotal();
      this.routerCheckAndPush(queryString);
      this.$emit("loaded");
    },
    goToDetail(item) {
      if (item.id) {
        this.$router.push({
          name: "AppealDetails",
          params: { id: item.id, theme: item.theme },
        });
      }
    },
    displayDelete({ id, theme }) {
      let that = this;
      this.$confirm({
        title: `Обращение "${theme}" будет удалено.`,
        content: `Будут удалены все сообщения. Продолжить?`,
        okType: "danger",
        onOk() {
          that.deleteRecord(id);
        },
      });
    },
    async deleteRecord(id) {
      try {
        let res = await this.deleteAppeal(id);
        if (res.status === 204) {
          this.$message.success("Обращение успешно удалено");
          await this.fetchAppeals();
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
      data: "appeals/getAppeals",
      userInfo: "auth/getUserInfo",
      areasAll: "skills/getAreasAll",
    }),
    areasForFilter() {
      return this.areasAll.map((area) => {
        return { value: area.id, text: area.name };
      });
    },
  },
  mounted() {
    this.$set(this.columns[1], "filters", this.areasForFilter);
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
    areasForFilter(values) {
      this.columns[1].filters = values;
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

.appeals-block
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
    .status-block
      text-align: center
      .status-block__tag
        margin-bottom: 5px
        margin-right: 0
      .status-block__text
        font-size: 0.8rem
    .pre-wrap
      white-space: pre-wrap
    .theme-block
      .message-count
        font-size: 12px
        color: #aaa
        margin: 0 0 -10px -3px
</style>
