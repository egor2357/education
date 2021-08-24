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
          <a-input
            v-if="field.type === 'text'"
            v-model="form[field.name]"
            @change="fieldChanged(field)"
            :ref="`field${index}`"
          />
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
  name: "AnnouncementsModal",
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
        caption: "",
        text: "",
      },
      title: "",
      layout: {
        labelCol: { span: 6 },
        wrapperCol: { span: 18 },
      },
      fields: [
        {
          name: "caption",
          label: "Тема",
          type: "text",
          validateStatus: "",
          help: "",
        },
        {
          name: "text",
          label: "Текст",
          type: "textarea",
          validateStatus: "",
          help: "",
        },
      ],
      rules: {
        caption: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите тему",
          },
        ],
        text: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите текст",
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
              dispatchName = "announcements/addAnnouncement";
              successCode = 201;
              successMessage = "Запись успешно добавлена";
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
      this.title += "Добавление записи";
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
