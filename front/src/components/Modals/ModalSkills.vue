<template>
  <a-modal
    :visible="true"
    :title="title"
    v-if="type !== 0"
    @cancel="handleCancel"
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
          <a-input-number
            v-else-if="field.type === 'number'"
            v-model="form[field.name]"
            @change="fieldChanged(field)"
            :min="0"
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
  name: "ModalSkills",
  props: {
    adding: {
      type: Boolean,
      default: true,
    },
    type: {
      type: Number,
    },
    editableData: Object,
  },
  data() {
    return {
      form: {
        name: null,
        number: null,
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
        {
          name: "number",
          label: "Номер",
          type: "number",
          validateStatus: "",
          help: "",
        },
      ],
      rules: {
        name: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите наименование",
          },
        ],
        number: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите номер",
          },
        ],
      },
      loadingButton: false,
    };
  },
  methods: {
    handleCancel() {
      this.form.name = null;
      this.form.number = null;
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

            if (this.type === 1 && this.adding) {
              dispatchName = "skills/addArea";
              successCode = 201;
              successMessage = "Образовательная область успешно добавлена";
            } else if (this.type === 1 && !this.adding) {
              dispatchName = "skills/editArea";
              successCode = 200;
              successMessage = "Образовательная область успешно изменена";
            } else if (this.type === 2 && this.adding) {
              dispatchName = "skills/addDirection";
              successCode = 201;
              successMessage = "Направление развития успешно добавлено";
            } else if (this.type === 2 && !this.adding) {
              dispatchName = "skills/editDirection";
              successCode = 200;
              successMessage = "Направлние развития успешно изменено";
            } else if (this.type === 3 && this.adding) {
              dispatchName = "skills/addSkill";
              successCode = 201;
              successMessage = "Навык успешно добавлен";
            } else if (this.type === 3 && !this.adding) {
              dispatchName = "skills/editSkill";
              successCode = 200;
              successMessage = "Навык успешно изменен";
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
      this.editableData.number
        ? (this.form.number = this.editableData.number)
        : "";
    }
    if (this.type === 1) {
      this.title += "образовательной области";
      this.editableData.lastNumberArea
        ? (this.form.number = this.editableData.lastNumberArea)
        : "";
    } else if (this.type === 2) {
      this.editableData.areaId
        ? (this.form.area_id = this.editableData.areaId)
        : "";
      this.editableData.lastNumberDirection
        ? (this.form.number = this.editableData.lastNumberDirection)
        : "";
      this.title += "направления развития";
    } else if (this.type === 3) {
      this.editableData.directionId
        ? (this.form.direction_id = this.editableData.directionId)
        : "";
      this.editableData.lastNumberSkill
        ? (this.form.number = this.editableData.lastNumberSkill)
        : "";
      this.title += "навыка";
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
