<template>
  <a-modal
    :visible="true"
    @cancel="handleCancel"
    @ok="handleOk"
    okText="Сохранить"
    cancelText="Отмена"
    :title="title"
    v-if="type !== 0"
    @confirmLoading="loadingButton"
  >
    <a-form-model :model="form" v-bind="layout" :rules="rules" ref="form">
      <template v-for="(field, index) in fields">
        <a-form-model-item
          :prop="field.name"
          :label="field.label"
          :key="field.name"
          :validateStatus="field.validateStatus"
          :help="field.help"
        >
          <a-input
            v-if="field.type === 'text'"
            v-model="form[field.name]"
            @change="fieldChanged(field)"
            :ref="`field${index}`"
          />
        </a-form-model-item>
      </template>
    </a-form-model>
  </a-modal>
</template>

<script>
export default {
  name: "ModalForm",
  props: {
    adding: {
      type: Boolean,
      default: true,
    },
    type: {
      type: [Number, String],
    },
    editableData: Object,
  },
  data() {
    return {
      form: {
        name: null,
      },
      title: "",
      layout: {
        labelCol: { span: 6 },
        wrapperCol: { span: 18 },
      },
      fields: [
        {
          name: "name",
          label: "Наименование",
          type: "text",
          validateStatus: "",
          help: "",
        },
      ],
      rules: {
        name: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите название",
          },
        ],
      },
      loadingButton: false,
    };
  },
  methods: {
    handleCancel() {
      this.form.name = null;
      this.$emit("close");
    },
    async handleOk() {
      this.loadingButton = true;
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          let dispatchName = "";
          let successCode = 0;
          let successMessage = "";

          if (this.type === 1 && this.adding) {
            dispatchName = "forms/addForm";
            successCode = 201;
            successMessage = "Форма проведения занятий успешно добавлена";
          } else if (this.type === 1 && !this.adding) {
            dispatchName = "forms/editForm";
            successCode = 200;
            successMessage = "Форма проведения занятий успешно изменена";
          } else if (this.type === 2 && this.adding) {
            dispatchName = "forms/addMethod";
            successCode = 201;
            successMessage = "Способ проведения занятий успешно добавлено";
          } else if (this.type === 2 && !this.adding) {
            dispatchName = "forms/editMethod";
            successCode = 200;
            successMessage = "Способ проведения занятий успешно изменено";
          }
          try {
            let res = await this.$store.dispatch(dispatchName, this.form);
            if (res.status === successCode) {
              this.$message.success(successMessage);
              this.$emit("closeSuccess");
            } else if (res.status === 400) {
              this.$message.error("Проверьте введённые данные");
              for (let key in res.data) {
                this.fields.forEach((field) => {
                  if (field.name === key) {
                    field.validateStatus = "error";
                    field.help = res.data[key];
                  }
                });
              }
            } else {
              this.$message.error("Произошла ошибка");
            }
          } catch (e) {
            this.$message.error("Произошла ошибка");
          } finally {
            this.loadingButton = false;
          }
        } else {
          return false;
        }
      });
    },
    fieldChanged(field) {
      field.validateStatus = "";
      field.help = "";
    },
    keydown(event) {
      if (
        event.type === "keydown" &&
        event.keyCode === 13 &&
        this.$refs.form !== undefined
      ) {
        this.handleOk();
      }
    },
  },
  created() {
    if (this.adding) {
      this.title += "Добавление ";
    } else {
      this.title += "Изменение ";
      this.editableData.id ? (this.form.id = this.editableData.id) : "";
      this.editableData.name ? (this.form.name = this.editableData.name) : "";
    }
    if (this.type === 1) {
      this.title += "формы проведения занятий";
    } else if (this.type === 2) {
      this.editableData.form_id
        ? (this.form.form_id = this.editableData.form_id)
        : "";
      this.title += "способа проведений занятий";
    }
    document.addEventListener("keydown", this.keydown);
  },
  mounted() {
    this.$nextTick(() => {
      this.$refs["field0"][0].focus();
    });
  },
  beforeDestroy() {
    document.removeEventListener("keydown", this.keydown);
  }
};
</script>

<style scoped></style>
