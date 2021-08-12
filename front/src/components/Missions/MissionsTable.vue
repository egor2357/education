<template>
  <a-table
    :columns="columns"
    :dataSource="data.results"
    bordered
    :rowKey="'id'"
    :pagination="pagination"
    @change="tableChanged"
  >
    <span slot="actions" slot-scope="text, item">
      <div class="flex-column">
        <a @click="$emit('displayEdit', item)" v-if="item.status !== 2">
          Изменить
        </a>
        <a @click="displayDelete(item)">Удалить</a>
        <a
          @click="setExecute(item.id)"
          v-if="
            item.status !== 2 &&
            (userInfo.id === item.director.id ||
              (item.controller && userInfo.id === item.controller.id))
          "
          >Завершить</a
        >
      </div>
    </span>
    <template slot="status" slot-scope="status">
      <a-tag v-if="status === 0" color="cyan">Новое</a-tag>
      <a-tag v-else-if="status === 1" color="purple">В процессе</a-tag>
      <a-tag v-else-if="status === 2" color="green">Исполнено</a-tag>
    </template>
  </a-table>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from "vuex";
import datetime from "@/mixins/datetime";
export default {
  name: "MissionsTable",
  mixins: [datetime],
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
          customRender: (date) => {
            return date ? this.formatDate(date) : "";
          },
        },
        {
          title: "Наименование",
          dataIndex: "caption",
          key: "caption",
        },
        {
          title: "Постановщик",
          dataIndex: "director.__str__",
          key: "director",
        },
        {
          title: "Исполнитель",
          dataIndex: "executor.__str__",
          key: "executor",
        },
        {
          title: "Контролёр",
          dataIndex: "controller.__str__",
          key: "controller",
        },
        {
          title: "Срок",
          dataIndex: "deadline",
          key: "deadline",
          customRender: (date) => {
            return date ? this.formatDate(date) : "";
          },
        },
        {
          title: "Статус",
          dataIndex: "status",
          key: "status",
          scopedSlots: { customRender: "status" },
        },
        {
          title: "Комментарий",
          dataIndex: "comment",
          key: "comment",
        },
        {
          title: "Действия",
          dataIndex: "actions",
          key: "actions",
          scopedSlots: { customRender: "actions" },
        },
      ],
    };
  },
  async created() {
    await this.getData();
    if (!this.userInfo.staff) {
      this.columns.splice(8);
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
      this.setQueryParams(
        `?page=${this.pagination.page}&per_page=${this.pagination.pageSize}`
      );
      await this.fetchMissions();
      this.$emit("loaded");
    },
    async tableChanged(pagination) {
      this.pagination.page = pagination.current;
      this.pagination.pageSize = pagination.pageSize;
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
  },
  computed: {
    ...mapGetters({
      data: "missions/getMissions",
      userInfo: "auth/getUserInfo",
    }),
  },
};
</script>

<style scoped></style>
