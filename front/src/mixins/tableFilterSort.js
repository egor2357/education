export default {
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
    };
  },
  methods: {
    updatePaginationTotal() {
      if (this.data.pagination) {
        this.pagination.total = this.data.pagination.count;
      }
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
    async tableChanged(pagination, filters, sorter) {
      this.filterQuery = "";
      this.columns.forEach((column) => {
        if (column.sortOrder && sorter.columnKey !== column.key) {
          column.sortOrder = false;
        } else if (sorter.columnKey === column.key && sorter.order === "descend") {
          column.sortOrder = "descend";
        } else if (sorter.columnKey === column.key && sorter.order === "ascend") {
          column.sortOrder = "ascend";
        } else if (sorter.columnKey === column.key && sorter.order === undefined) {
          column.sortOrder = false;
        }
      });
      if (sorter.order) {
        sorter.order === "ascend"
          ? (this.filterQuery += `&ordering=${sorter.column.key}`)
          : (this.filterQuery += `&ordering=-${sorter.column.key}`);
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
    routerCheckAndPush(queryString = "") {
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
  },
};
