<template>
  <a-modal :visible="true" :title="title" @cancel="handleCancel">
    <a-form-model :model="form" v-bind="layout" :rules="rules" ref="form">
      <template v-for="(field, index) in fields">
        <a-form-model-item
          :prop="field.name"
          :label="field.label"
          :key="field.name"
          :validateStatus="field.validateStatus"
          :help="field.help"
        >
          <a-textarea
            v-if="field.type === 'textarea'"
            v-model="form[field.name]"
            @change="fieldChanged(field)"
            :ref="`field${index}`"
            :rows="4"
          />
        </a-form-model-item>
      </template>
    </a-form-model>
    <template slot="footer">
      <a-button @click="handleCancel"> Отмена </a-button>
      <a-button
        type="primary"
        :loading="loadingButton"
        :disabled="loadingButton"
        @click="handleOk"
      >
        {{ loadingButton ? "Загрузка..." : "Сохранить" }}
      </a-button>
    </template>
  </a-modal>
</template>

<script>
export default {
  name: "AppealsModal",
  props: {
    adding: {
      type: Boolean,
      default: true,
    },
    editableData: Object,
  },
  data() {
    return {
      form: {
        theme: "",
      },
      title: "",
      layout: {
        labelCol: { span: 4 },
        wrapperCol: { span: 20 },
      },
      fields: [
        {
          name: "theme",
          label: "Тема",
          type: "textarea",
          validateStatus: "",
          help: "",
        },
      ],
      rules: {
        theme: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите тему обращения",
          },
        ],
      },
      loadingButton: false,
    };
  },
  methods: {
    handleCancel() {
      this.$emit("close");
    },
    async handleOk() {
      if (!this.loadingButton) {
        this.$refs.form.validate(async (valid) => {
          if (valid) {
            this.loadingButton = true;
            let dispatchName = "";
            let successCode = 0;
            let successMessage = "";

            if (this.adding) {
              dispatchName = "appeals/addAppeal";
              successCode = 201;
              successMessage = "Обращение к руководству успешно добавлено";
            } else {
              dispatchName = "appeals/editAppeal";
              successCode = 200;
              successMessage = "Обращение к руководству успешно изменено";
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
      }
    },
    fieldChanged(field) {
      field.validateStatus = "";
      field.help = "";
    },
    keydown(event) {
      if (
        event.type === "keydown" &&
        event.keyCode === 13 &&
        this.$refs.form !== undefined &&
        event.srcElement.localName !== "textarea"
      ) {
        this.handleOk();
      }
    },
  },
  created() {
    if (this.adding) {
      this.title += "Добавление обращения к руководству";
    } else {
      this.title += "Изменение обращения к руководству";
      this.editableData.id ? (this.form.id = this.editableData.id) : "";
      this.editableData.theme
        ? (this.form.theme = this.editableData.theme)
        : (this.form.theme = "");
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
  },
};
</script>

<style scoped></style>
