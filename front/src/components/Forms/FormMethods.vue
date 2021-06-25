<template>
  <a-collapse>
    <a-collapse-panel
      :key="form.id"
      :header="form.name"
      v-for="form in forms"
      :showArrow="form.methods.length !== 0"
      :class="{ 'panel-empty': form.methods.length === 0 }"
    >
      <div v-for="method in form.methods" :key="method.id" class="method">
        <span>{{ method.name }}</span>
        <span style="float: right">
          <a @click.stop="$emit('displayEdit', 2, method)">Изменить</a>
          <a-divider type="vertical" />
          <a @click.stop="displayDelete(method, 2)">Удалить</a>
        </span>
      </div>
      <template slot="extra">
        <a @click.stop="$emit('displayAdd', 2, form.id)">Добавить способ</a>
        <a-divider type="vertical" />
        <a @click.stop="$emit('displayEdit', 1, form)"> Изменить </a>
        <a-divider type="vertical" />
        <a @click.stop="displayDelete(form, 1)">Удалить</a>
      </template>
    </a-collapse-panel>
  </a-collapse>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
  name: "FormMethods",
  data() {
    return {};
  },
  computed: {
    ...mapGetters({
      forms: "forms/getForms",
    }),
  },
  methods: {
    ...mapActions({
      deleteForm: "forms/deleteForm",
      deleteMethod: "forms/deleteMethod",
    }),
    async deleteRecord(id, type) {
      let dispatchName = "";
      let successMessage = "";
      if (type === 1) {
        dispatchName = "forms/deleteForm";
        successMessage = "Форма проведения занятий успешно удалена";
      } else if (type === 2) {
        dispatchName = "forms/deleteMethod";
        successMessage = "Способ проведения занятий успешно удален";
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
    displayDelete({ id, name }, type) {
      let title = "";
      if (type === 1) {
        title += `Форма проведения занятий "${name}" будет удалена?`;
      } else if (type === 2) {
        title += `Способ проведения занятий "${name}" будет удален?`;
      }
      let that = this;
      this.$confirm({
        title: title,
        content: `Продолжить?`,
        okType: "danger",
        onOk() {
          that.deleteRecord(id, type);
        },
      });
    },
  },
};
</script>

<style lang="sass">
.forms
  .ant-collapse
    .ant-collapse-item
      &.panel-empty
        .ant-collapse-header
          cursor: default
        .ant-collapse-content
          border-top: none
  .ant-collapse-content-box
    padding: 0 10px !important
    .method
      padding: 10px 10px
      &:not(:last-child)
        border-bottom: 1px solid #d9d9d9
</style>
