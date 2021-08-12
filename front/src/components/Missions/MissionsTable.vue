<template>
  <div>
    <a-button type="primary" @click="displayForm(true)" v-if="!viewOnly">
      Добавить
    </a-button>
    <a-divider />
    <a-spin :spinning="loading">
      <a-table
        :columns="columns"
        :dataSource="data.results"
        bordered
        :rowKey="'id'"
        :pagination="pagination"
        @change="tableChanged"
      >
        <span slot="actions" slot-scope="text, item">
          <a @click="editRow(item)"> Изменить </a>
          <a-divider type="vertical" />
          <a-popconfirm
            title="Вы действительно хотите удалить поручение"
            ok-text="Да"
            cancel-text="Нет"
            @confirm="displayDelete(item)"
          >
            <a>Удалить</a>
          </a-popconfirm>
        </span>
      </a-table>
    </a-spin>
  </div>
</template>

<script>
export default {
  name: "MissionsTable",
  data() {
    return {
      loading: true
    }
  },
  methods: {
    tableChanged(e) {
      console.log(e)
    },
    displayDelete({ id, caption }, type) {
      let that = this;
      this.$confirm({
        title: `Поручение "${caption} будет удалено."`,
        content: `Продолжить?`,
        okType: "danger",
        onOk() {
          that.deleteRecord(id, type);
        },
      });
    },
    async deleteRecord(id, type) {
      let dispatchName = "";
      let successMessage = "";
      if (type === 1) {
        dispatchName = "forms/deleteForm";
        successMessage = "Метод проведения занятий успешно удален";
      } else if (type === 2) {
        dispatchName = "forms/deleteMethod";
        successMessage = "Форма проведения занятий успешно удалена";
      } else {
        return;
      }
      try {
        let res = await this.$store.dispatch(dispatchName, id);
        if (res.status === 204) {
          this.$message.success(successMessage);
          this.$emit("needUpdate");
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      }
    },
  },
};
</script>

<style scoped></style>
